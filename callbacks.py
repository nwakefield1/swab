import discord


class PafyCallback():
    def __init__(self, file_path, vc, helper):
        self.vc = vc
        self.file_path = file_path
        self.helper = helper

    def __call__(self, total, recvd, ratio, rate, eta):
        if ratio == 1.0:        
            audio = discord.FFmpegOpusAudio(self.file_path)
            self.helper.songs.put((self.vc, audio))

            # self.vc.play(audio)
