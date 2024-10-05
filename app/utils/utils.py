from aiogram.types import Message
import json
from uuid import uuid4

import os
import logging

logger = logging.getLogger(__name__)


class CodeManager:
    

    def generate_code(self):
        
        
        code = str(uuid4())[:4]
        
        # Save code
        
        logger.info("New code generated: %s", code)
        
        self.add_code(code)
        return code

    def is_available_code(code):
        
        with open(path, 'r') as f:
            codes = json.load(f)
            if code in codes:
                return True
            else:
                return False
            
    def add_code(code):

        with open(path, 'r') as f:
            codes : list = json.load(f)
            codes.append(code)
            
        with open(path, 'w') as f:
            json.dump(codes, f)
            
    def get_codes():
            
        with open(path, 'r') as f:
            codes = json.load(f)
            return codes
            
    def remove_code(code):

        with open(path, 'r') as f:
            codes : list= json.load(f)
            codes.remove(code)
            
        with open(path, 'w') as f:
            json.dump(codes, f)
            
    def count_codes():
            
        with open(path, 'r') as f:
            codes = json.load(f)
            return len(codes)
            

def is_convertible_to_int(value: str) -> bool:
    try:
        int(value)
        return True
    except ValueError:
        return False


def get_media_type(message: Message) -> str:
    
    if message.photo:
        return "image"
    elif message.video:
        return "video"
    elif message.audio:
        return "audio"
    elif message.video_note:
        return "video_note"
    else:
        return "text"
    
async def save_media(message: Message):
    from app.core.bot import bot
    
    if message.photo:
        file_id = message.photo[-1].file_id
        await bot.download(file_id, "app/database/medias/images/{}.jpg".format(file_id))
        return "photo", "app/database/medias/images/{}.jpg".format(file_id)

    if message.video:
        file_id = message.video.file_id
        await bot.download(file_id, "app/database/medias/videos/{}.mp4".format(file_id))
        return "video", "app/database/medias/videos/{}.mp4".format(file_id)
        
    if message.video_note:
        file_id = message.video_note.file_id
        await bot.download(file_id, "app/database/medias/video_notes/{}.mp4".format(file_id))
        return "video_note", "app/database/medias/video_notes/{}.mp4".format(file_id)
        
    if message.voice:
        file_id = message.voice.file_id   
        await bot.download(file_id, "app/database/medias/voices/{}.ogg".format(file_id))
        return "voice", "app/database/medias/voices/{}.ogg".format(file_id)
    
    if message.audio:
        print(message.audio)
        file_id = message.audio.file_id
        await bot.download(file_id, "app/database/medias/audios/{}.ogg".format(file_id))
        return "audio", "app/database/medias/audios/{}.ogg".format(file_id)
        
    else: # text
        with open("app/database/medias/texts/{}.txt".format(message.message_id), "w", encoding="utf-8") as f:
            f.write(message.text)
        return "text", "app/database/medias/texts/{}.txt".format(message.message_id)



if __name__ == "__main__":
    pass