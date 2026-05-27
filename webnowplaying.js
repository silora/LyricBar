// NAME: WebNowPlaying
// AUTHOR: khanhas, keifufu
// DESCRIPTION: Provides media information and controls to WebNowPlaying-Redux-Rainmeter, but also supports WebNowPlaying for Rainmeter 0.5.0 and older.

/// <reference path="../globals.d.ts" />

(function WebNowPlaying() {
	if (!Spicetify.CosmosAsync || !Spicetify.Platform.LibraryAPI) {
		setTimeout(WebNowPlaying, 500);
		return;
	}

	const socket = new WNPReduxWebSocket();
	window.addEventListener("beforeunload", () => {
		socket.close();
	});
})();

class WNPReduxWebSocket {
	_ws = null;
	cache = new Map();
	reconnectCount = 0;
	updateInterval = null;
	tickRaf = null;
	communicationRevision = null;
	connectionTimeout = null;
	reconnectTimeout = null;
	isClosed = false;
	spicetifyInfo = {
		player: "Spotify Desktop",
		state: "STOPPED",
		title: "",
		artist: "",
		album: "",
		cover: "",
		duration: "0:00",
		position: "0:00",
		type: "",
		uid: "",
		begintime: 0,
	};
	isResetting = false;
	lastNext = false;

	constructor() {
		this.init();

		this.tick = this.tick.bind(this);
		this.tick();

		Spicetify.Player.addEventListener("songchange", ({ data }) => {
			setTimeout(() => this.restartPlayer(data), 1000);
		});

		Spicetify.Player.addEventListener("onplaypause", ({ data }) => {
			if (this.isResetting) return;
			this.updateSpicetifyInfo(data);
		});

		Spicetify.Player.addEventListener("onprogress", ({ data }) => {
			this.updateSpicetifyInfo(data);
		});
	}

	tick() {
		if (!this.isClosed && !this.isResetting && Spicetify.Player?.data) {
			this.updateProgressOnly();
			this.sendUpdate();
		}

		this.tickRaf = requestAnimationFrame(this.tick);
	}

	updateProgressOnly() {
		try {
			const progress = Spicetify.Player.getProgress();
			if (typeof progress === "number" && !Number.isNaN(progress)) {
				this.spicetifyInfo.position = timeInSecondsToString(
					Math.round(progress / 1000)
				);
			}
		} catch {}
	}

	async restartPlayer(data) {
		this.isResetting = true;
		this.updateSpicetifyInfo(Spicetify.Player.data);

		Spicetify.Player.pause();
		Spicetify.Player.play();

		await new Promise(resolve => setTimeout(resolve, 500));

		this.isResetting = false;
		this.updateSpicetifyInfo(Spicetify.Player.data);
	}

	updateSpicetifyInfo(data) {
		if (!data?.item?.metadata) return;
		if (this.isResetting) return;

		const meta = data.item.metadata;

		this.spicetifyInfo.title = meta.title;
		this.spicetifyInfo.album = meta.album_title;
		this.spicetifyInfo.duration = meta.duration;
		this.spicetifyInfo.state = !data.isPaused ? "PLAYING" : "PAUSED";
		this.spicetifyInfo.artist = meta.artist_name;
		this.spicetifyInfo.uid = data.item.uri.split(":").pop(-1);
		this.spicetifyInfo.begintime =
			Spicetify.Player.data.timestamp -
			Spicetify.Player.data.positionAsOfTimestamp;
		this.spicetifyInfo.type = data.item.type;

		this.updateProgressOnly();

		if (!this.spicetifyInfo.artist) {
			this.spicetifyInfo.artist = meta.album_title;
		}

		const cover = meta.image_xlarge_url;
		if (cover?.indexOf("localfile") === -1) {
			this.spicetifyInfo.cover =
				`https://i.scdn.co/image/${cover.substring(cover.lastIndexOf(":") + 1)}`;
		} else {
			this.spicetifyInfo.cover = "";
		}

		this.sendUpdate();
	}

	init() {
		try {
			this._ws = new WebSocket("ws://127.0.0.1:8974");
			this._ws.onopen = this.onOpen.bind(this);
			this._ws.onclose = this.onClose.bind(this);
			this._ws.onerror = this.onError.bind(this);
			this._ws.onmessage = this.onMessage.bind(this);
		} catch {
			this.retry();
		}
	}

	close(cleanupOnly = false) {
		if (!cleanupOnly) this.isClosed = true;

		this.cache = new Map();
		this.communicationRevision = null;

		if (this.updateInterval) clearInterval(this.updateInterval);
		if (this.reconnectTimeout) clearTimeout(this.reconnectTimeout);
		if (this.connectionTimeout) clearTimeout(this.connectionTimeout);
		if (this.tickRaf) cancelAnimationFrame(this.tickRaf);

		if (this._ws) {
			this._ws.onclose = null;
			this._ws.close();
		}
	}

	retry() {
		if (this.isClosed) return;

		this.close(true);

		this.reconnectTimeout = setTimeout(
			() => {
				this.init();
				this.reconnectAttempts += 1;
			},
			Math.min(
				1000 * (this.reconnectAttempts <= 30 ? 1 : 2 ** (this.reconnectAttempts - 30)),
				60000
			)
		);
	}

	send(data) {
		if (!this._ws || this._ws.readyState !== WebSocket.OPEN) return;
		this._ws.send(data);
	}

	onOpen() {
		this.reconnectCount = 0;

		// 保留原来的发送机制，不改 socket 协议
		this.updateInterval = setInterval(this.sendUpdate.bind(this), 500);

		this.connectionTimeout = setTimeout(() => {
			if (this.communicationRevision === null) {
				this.communicationRevision = "legacy";
			}
		}, 1000);
	}

	onClose() {
		this.retry();
	}

	onError() {
		this.retry();
	}

	onMessage(event) {
		if (this.communicationRevision) {
			switch (this.communicationRevision) {
				case "legacy":
					OnMessageLegacy(this, event.data);
					break;
				case "1":
					OnMessageRev1(this, event.data);
					break;
			}

			this.sendUpdate();
		} else {
			if (event.data.startsWith("Version:")) {
				this.communicationRevision = "legacy";
			} else if (event.data.startsWith("ADAPTER_VERSION ")) {
				this.communicationRevision = event.data.split(";")[1].split(" ")[1];
			} else {
				this.communicationRevision = "legacy";
			}
		}
	}

	sendUpdate() {
		if (!this._ws || this._ws.readyState !== WebSocket.OPEN) return;

		switch (this.communicationRevision) {
			case "legacy":
				SendUpdateLegacy(this);
				break;
			case "1":
				SendUpdateRev1(this);
				break;
		}
	}
}

function OnMessageLegacy(self, message) {
	try {
		const [type, data] = message.toUpperCase().split(" ");

		switch (type) {
			case "PLAYPAUSE": {
				Spicetify.Player.togglePlay();
				self.spicetifyInfo.state =
					self.spicetifyInfo.state === "PLAYING" ? "PAUSED" : "PLAYING";
				break;
			}

			case "NEXT":
				Spicetify.Player.next();
				break;

			case "PREVIOUS":
				Spicetify.Player.back();
				break;

			case "SETPOSITION": {
				const [, positionPercentage] =
					message.toUpperCase().split(":")[1].split("SETPROGRESS ");
				Spicetify.Player.seek(Number.parseFloat(positionPercentage.replace(",", ".")));
				break;
			}

			case "SETVOLUME":
				Spicetify.Player.setVolume(Number.parseInt(data) / 100);
				break;

			case "REPEAT": {
				Spicetify.Player.toggleRepeat();
				self.spicetifyInfo.repeat =
					self.spicetifyInfo.repeat === "NONE"
						? "ALL"
						: self.spicetifyInfo.repeat === "ALL"
							? "ONE"
							: "NONE";
				break;
			}

			case "SHUFFLE": {
				Spicetify.Player.toggleShuffle();
				self.spicetifyInfo.shuffle = !self.spicetifyInfo.shuffle;
				break;
			}

			case "TOGGLETHUMBSUP": {
				Spicetify.Player.toggleHeart();
				self.spicetifyInfo.rating = self.spicetifyInfo.rating === 5 ? 0 : 5;
				break;
			}

			case "RATING": {
				const rating = Number.parseInt(data);
				const isLiked = self.spicetifyInfo.rating > 3;

				if (rating >= 3 && !isLiked) {
					Spicetify.Player.toggleHeart();
				} else if (rating < 3 && isLiked) {
					Spicetify.Player.toggleHeart();
				}

				self.spicetifyInfo.rating = rating;
				break;
			}
		}
	} catch (e) {
		self.send(`Error:Error sending event to ${self.spicetifyInfo.player}`);
		self.send(`ErrorD:${e}`);
	}
}

function SendUpdateLegacy(self) {
	if (self.isResetting) return;

	if (!Spicetify.Player.data && self.cache.get("state") !== 0) {
		self.cache.set("state", 0);
		self.send("STATE:0");
		return;
	}

	self.updateProgressOnly();

	self.spicetifyInfo.begintime =
		Spicetify.Player.data.timestamp -
		Spicetify.Player.data.positionAsOfTimestamp;

	let need_update = false;
	const update = {};

	for (const key of Object.keys(self.spicetifyInfo)) {
		try {
			let value = self.spicetifyInfo[key];

			if (key === "state") {
				value =
					value === "PLAYING"
						? 1
						: value === "PAUSED"
							? 2
							: 0;
			}

			if (value !== null && value !== self.cache.get(key)) {
				self.cache.set(key, value);
				need_update = true;
			}

			update[key.toUpperCase()] = value;
		} catch (e) {
			self.send(`Error: Error updating ${key} for ${self.spicetifyInfo.player}`);
			self.send(`ErrorD:${e}`);
		}
	}

	if (need_update) {
		self.send(JSON.stringify(update));
	}
}

function OnMessageRev1(self, message) {
	const [type, data] = message.split(" ");

	try {
		switch (type) {
			case "TOGGLE_PLAYING": {
				Spicetify.Player.togglePlay();
				self.spicetifyInfo.state =
					self.spicetifyInfo.state === "PLAYING" ? "PAUSED" : "PLAYING";
				break;
			}

			case "NEXT":
				Spicetify.Player.next();
				break;

			case "PREVIOUS":
				Spicetify.Player.back();
				break;

			case "SET_POSITION": {
				const [, positionPercentage] = data.split(":");
				Spicetify.Player.seek(Number.parseFloat(positionPercentage.replace(",", ".")));
				break;
			}

			case "SET_VOLUME":
				Spicetify.Player.setVolume(Number.parseInt(data) / 100);
				break;

			case "TOGGLE_REPEAT": {
				Spicetify.Player.toggleRepeat();
				self.spicetifyInfo.repeat =
					self.spicetifyInfo.repeat === "NONE"
						? "ALL"
						: self.spicetifyInfo.repeat === "ALL"
							? "ONE"
							: "NONE";
				break;
			}

			case "TOGGLE_SHUFFLE": {
				Spicetify.Player.toggleShuffle();
				self.spicetifyInfo.shuffle = !self.spicetifyInfo.shuffle;
				break;
			}

			case "TOGGLE_THUMBS_UP": {
				Spicetify.Player.toggleHeart();
				self.spicetifyInfo.rating = self.spicetifyInfo.rating === 5 ? 0 : 5;
				break;
			}

			case "SET_RATING": {
				const rating = Number.parseInt(data);
				const isLiked = self.spicetifyInfo.rating > 3;

				if (rating >= 3 && !isLiked) {
					Spicetify.Player.toggleHeart();
				} else if (rating < 3 && isLiked) {
					Spicetify.Player.toggleHeart();
				}

				self.spicetifyInfo.rating = rating;
				break;
			}
		}
	} catch (e) {
		self.send(`ERROR Error sending event to ${self.spicetifyInfo.player}`);
		self.send(`ERRORDEBUG ${e}`);
	}
}

function SendUpdateRev1(self) {
	if (!Spicetify.Player.data && self.cache.get("state") !== "STOPPED") {
		self.cache.set("state", "STOPPED");
		self.send("STATE STOPPED");
		return;
	}

	self.updateProgressOnly();

	for (const key of Object.keys(self.spicetifyInfo)) {
		try {
			let value = self.spicetifyInfo[key];

			if (typeof value === "number") {
				value = Math.round(value);
			}

			if (value !== null && value !== self.cache.get(key)) {
				self.send(`${key.toUpperCase()} ${value}`);
				self.cache.set(key, value);
			}
		} catch (e) {
			self.send(`ERROR Error updating ${key} for ${self.spicetifyInfo.player}`);
			self.send(`ERRORDEBUG ${e}`);
		}
	}
}

function pad(num, size) {
	return num.toString().padStart(size, "0");
}

function timeInSecondsToString(timeInSeconds) {
	const timeInMinutes = Math.floor(timeInSeconds / 60);

	if (timeInMinutes < 60) {
		return `${timeInMinutes}:${pad(Math.floor(timeInSeconds % 60), 2)}`;
	}

	return `${Math.floor(timeInMinutes / 60)}:${pad(Math.floor(timeInMinutes % 60), 2)}:${pad(Math.floor(timeInSeconds % 60), 2)}`;
}