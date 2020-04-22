import discord


class PafyCallback():
    # def __init__(self, swab_helper, file_path, vc):
    #     self.swab_helper = swab_helper
    #     self.vc = vc
    #     self.file_path = file_path

    def __init__(self, music, file_path, voice_client):
        self.music = music
        self.file_path = file_path
        self.voice_client = voice_client

    def __call__(self, total, recvd, ratio, rate, eta):
        if ratio == 1.0:
            self.music.add_to_queue(self.file_path)
            if not self.voice_client.is_playing():
                self.music.play_song(self.voice_client)      
          
        #     audio = discord.FFmpegOpusAudio(self.file_path)
        #     self.vc.play(audio)
