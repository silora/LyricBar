
import logging
import re
from typing import Optional
import syncedlyrics
from syncedlyrics.utils import R_FEAT, generate_bs4_soup
import rapidfuzz
from bs4 import SoupStrainer

INSTRUMENTAL_LRC = "[00:00.00]  ♬"

def _str_score(a, b):
    a, b = a.lower(), b.lower()
    if "feat" not in b:
        a, b = R_FEAT.sub("", a), R_FEAT.sub("", b)
    return (rapidfuzz.fuzz.token_set_ratio(a, b), rapidfuzz.fuzz.ratio(a, b))

def _str_same(a, b, n):
    score = _str_score(a, b)
    return round(score[0]) >= n

syncedlyrics.utils.str_score = _str_score
syncedlyrics.utils.str_same = _str_same

def _sort_results_with_length(
    results,
    search_term,
    string_key = "name",
    length_key = "length",
):
    if isinstance(string_key, str):
        string_key = lambda t: t[string_key]
    if isinstance(length_key, str):
        length_key = lambda t: t[length_key]
    sort_key = lambda t: ((length_key(t), *_str_score(string_key(t), search_term)), length_key(t))
    return sorted(results, key=sort_key, reverse=True)

def _get_best_match_with_length(
    results,
    search_term,
    string_key,
    length_key,
    min_score = 80,
):
    if not results:
        return None
    results = _sort_results_with_length(results, search_term, string_key=string_key, length_key=length_key)
    best_match = results[0]

    value_to_compare = (
        best_match[string_key]
        if isinstance(string_key, str)
        else string_key(best_match)
    )
    
    if not _str_same(value_to_compare, search_term, n=min_score):
        return None
    return best_match


from syncedlyrics.providers import Deezer, Lrclib, Musixmatch, NetEase, Megalobiz, Genius

def _get_lrc_musixmatch(self, t):
    search_term = f"{t.title} {t.artist}"
    r = self._get(
            "track.search",
            [
                ("q", search_term),
                ("page_size", "10"),
                ("page", "1"),
            ],
        )
    status_code = r.json()["message"]["header"]["status_code"]
    if status_code != 200:
        self.logger.warning(f"Got status code {status_code} for {search_term}")
        return None
    body = r.json()["message"]["body"]
    tracks = body["track_list"]
    cmp_key = lambda _: f"{_['track']['track_name']} {_['track']['artist_name']}"
    track_len_diff = lambda _: - abs(_["track"]["track_length"] - int(t.length)/1000)
    track = _get_best_match_with_length(tracks, search_term, cmp_key, track_len_diff)
    if not track:
        return None
    if track["track"]["instrumental"] == 1:
        return INSTRUMENTAL_LRC
    track_id = track["track"]["track_id"]
    if self.enhanced:
        return self.get_lrc_word_by_word(track_id) or self.get_lrc_by_id(track_id)
    else:
        return self.get_lrc_by_id(track_id)
Musixmatch.get_lrc = _get_lrc_musixmatch

def _get_lrc_lrclib(self, t):
    search_term = f"{t.title} {t.artist}"
    url = self.SEARCH_ENDPOINT
    r = self.session.get(url, params={"q": search_term})
    if not r.ok:
        return None
    tracks = r.json()
    if not tracks:
        return None
    tracks = _sort_results_with_length(
        tracks, search_term, lambda _: f'{_["artistName"]} - {_["trackName"]}', lambda _: 0 - abs(_["duration"] - int(t.length)/1000)
    )
    _id = None
    for track in tracks:
        if (track.get("syncedLyrics", "") or "").strip():
            return track.get("syncedLyrics", track.get("plainLyrics"))
    return None
Lrclib.get_lrc = _get_lrc_lrclib

def _search_track_netease(self, t):
    search_term = f"{t.title} {t.artist}"
    params = {"limit": 10, "type": 1, "offset": 0, "s": search_term}
    response = self.session.get(self.API_ENDPOINT_METADATA, params=params)
    results = response.json().get("result", {}).get("songs")
    if not results:
        return None
    cmp_key = lambda _: f"{_.get('name')} {_.get('artists')[0].get('name')}"
    track = _get_best_match_with_length(results, search_term, cmp_key, lambda _: 0 - abs(_["duration"]/1000 - int(t.length)/1000))
    self.session.cookies.update(response.cookies)
    self.session.headers.update({"referer": response.url})
    return track
NetEase.search_track = _search_track_netease

def _get_lrc_netease(self, t):
    track = self.search_track(t)
    if not track:
        return None
    return self.get_lrc_by_id(track["id"])
NetEase.get_lrc = _get_lrc_netease

def _get_lrc_deezer(self, t):
    search_term = f"{t.title} {t.artist}"
    url = self.SEARCH_ENDPOINT + search_term.replace(" ", "+")
    search_results = self.session.get(url).json()
    cmp_key = lambda _: f"{_.get('title')} {_.get('artist').get('name')}"
    track = _get_best_match_with_length(search_results.get("data", []), search_term, cmp_key, lambda _: 0 - abs(_["duration"] - int(t.length)/1000))
    if not track:
        return None
    return self.get_lrc_by_id(track["id"])
Deezer.get_lrc = _get_lrc_deezer

def _get_lrc_megalobiz(self, t):
    search_term = f"{t.title} {t.artist}"
    url = self.SEARCH_ENDPOINT.format(q=search_term.replace(" ", "+"))

    def _href_match(h: Optional[str]):
        if h and h.startswith("/lrc/maker/"):
            return True
        return False

    a_tags_boud = SoupStrainer("a", href=href_match)
    soup = generate_bs4_soup(self.session, url, parse_only=a_tags_boud)

    candidates = []
    for a in soup.find_all("a"):
        match = re.search(r"(^.*)(\[\d\d:\d\d\.\d\d\])", a.get("title", ""))
        if not match:
            continue
        length = match.group(2)
        length = int(length[1:3]) * 60 + int(length[4:6]) + int(length[7:9]) / 100
        candidates.append({
            "raw": a,
            "name": match.group(1),
            "length": length
        })
    a_tag = _get_best_match_with_length(candidates, search_term, lambda _: _["name"], lambda _: _["length"] - int(t.length)/1000)
    if not a_tag:
        return None
    # Scraping from the LRC page
    lrc_id = a_tag["raw"]["href"].split(".")[-1]
    soup = generate_bs4_soup(self.session, self.ROOT_URL + a_tag["raw"]["href"])
    return soup.find("div", {"id": f"lrc_{lrc_id}_details"}).get_text()
Megalobiz.get_lrc = _get_lrc_megalobiz

logger = logging.getLogger(__name__)


def _is_lrc_valid_crude(
    lrc, allow_plain_format=False, check_translation=False
) :
    if not lrc:
        return False
    lines = lrc.split("\n")
    if len(lines) > 10:
        lines = lines[5:10]
    if not allow_plain_format:
        if not check_translation:
            conds = ["[" in l for l in lines]
            return all(conds)
        else:
            for i, line in enumerate(lines):
                if "[" in line:
                    if i + 1 < len(lines):
                        next_line = lines[i + 1]
                        if "(" not in next_line:
                            return False
    return True


def _search(
    search_track,
    allow_plain_format=False,
    providers=None,
    lang=None,
    enhanced=False,
):
    _providers = [] 
    for provider in providers:
        if provider.lower() == "musixmatch":
            _providers.append(Musixmatch(lang=lang, enhanced=enhanced))
        elif provider.lower() == "lrclib":
            _providers.append(Lrclib())
        elif provider.lower() == "deezer":
            _providers.append(Deezer())
        elif provider.lower() == "netease":
            _providers.append(NetEase())
        elif provider.lower() == "megalobiz":
            _providers.append(Megalobiz())
        elif provider.lower() == "genius":
            _providers.append(Genius())
    if _providers == []:
        return None

    lrc = None
    for provider in _providers:
        logger.debug(f"Looking for an LRC on {provider.__class__.__name__}")
        try:
            _l = provider.get_lrc(search_track)
        except Exception as e:
            logger.error(
                f"An error occurred while searching for an LRC on {provider.__class__.__name__}"
            )
            logger.error(e)
            continue
        if enhanced and not _l:
            # Since enhanced is only supported by Musixmatch, break if no LRC is found
            break
        check_translation = lang is not None and isinstance(provider, Musixmatch)
        if _is_lrc_valid_crude(_l, allow_plain_format, check_translation):
            logger.info(
                f'synced-lyrics found for "{search_track}" on {provider.__class__.__name__}'
            )
            lrc = _l
            break
        else:
            logger.debug(
                f"Skip {provider.__class__.__name__} as the synced-lyrics is not valid. (allow_plain_format={allow_plain_format})"
            )
            logger.debug(f"Lyrics: {_l}")
    if not lrc:
        logger.info(f'No synced-lyrics found for "{search_track}" :(')
        return None
    return lrc

syncedlyrics.search = _search

print("Patched syncedlyrics")