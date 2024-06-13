class PafyCallback:
    def __init__(self, music, file_path, voice_client):
        self.music = music
        self.file_path = file_path
        self.voice_client = voice_client

    async def __call__(self, total, recvd, ratio, rate, eta):
        if ratio == 1.0:
            self.music.add_to_queue(self.file_path)
            if not self.voice_client.is_playing():
                await self.music.play_song(self.voice_client)
