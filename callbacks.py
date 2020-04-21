import discord


class PafyCallback():
    def __init__(self, file_path, vc):
        self.vc = vc
        self.file_path = file_path

    def __call__(self, total, recvd, ratio, rate, eta):
        if ratio == 1.0:        
            audio = discord.FFmpegOpusAudio(self.file_path)
            self.vc.play(audio)
