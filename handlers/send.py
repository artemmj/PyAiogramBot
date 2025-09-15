import asyncio
import logging
import os

from aiogram import Router
from aiogram.types import FSInputFile, InputMediaVideo, InputMediaPhoto
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender

from keyboards.all_kbs import main_kb
from keyboards.inline_kbs import get_inline_kb
from settings import bot, media_dir

logger = logging.getLogger('_handler_send')
send_files_router = Router()


@send_files_router.message(Command('send_audio'))
async def send_audio(message: Message, state: FSMContext):
    audio_file = FSInputFile(path=os.path.join(media_dir, 'sample-6s.mp3'))

    # await message.answer_audio(audio=audio_file)
    s_msg = await message.answer_audio(
        audio=audio_file,
        reply_markup=main_kb(message.from_user.id),
        caption='Моя <u>отформатированная</u> подпись к <b>файлу</b>',
    )
    logger.info(s_msg.message_id)
    logger.info(s_msg.audio.file_id)
    logger.info(s_msg.audio.file_name)


@send_files_router.message(Command('send_photo'))
async def send_photo(message: Message, state: FSMContext):
    photo_file = FSInputFile(path=os.path.join(media_dir, '1.png'))
    photo_id = 'AgACAgIAAxkDAAICqWjIdmQ_sKA0x2blooesFX-XvjGVAAKCCjIbavhJSkU2EflnrXraAQADAgADeAADNgQ'
    photo_url = 'https://indirimlerce.com/wp-content/uploads/2023/02/phyton-ile-neler-yapilabilir.jpg'

    s_msg = await message.answer_photo(
        photo=photo_file,
        reply_markup=main_kb(message.from_user.id),
        caption='Это <b>ОЧЕНЬ ОПАСНЫЙ</b> чувак!',
    )
    logger.info(s_msg.photo[-1].file_id)


@send_files_router.message(Command('send_video'))
async def send_video(message: Message, state: FSMContext):
    video_file = FSInputFile(path=os.path.join(media_dir, 'sample.mp4'))
    # s_msg = await message.answer_video(
    #     video=video_file,
    #     # reply_markup=main_kb(message.from_user.id),
    #     caption='Моя отформатированная подпись к файлу',
    # )
    # await asyncio.sleep(1.5)
    # await s_msg.edit_caption(caption='Новое описание к моему видео.')

    s_msg = await message.answer_video(
        video=video_file,
        reply_markup=main_kb(message.from_user.id),
        caption='Моя отформатированная подпись к файлу',
    )
    await asyncio.sleep(2)
    s_video = await message.answer_video(
        video=s_msg.video.file_id,
        caption='Новое описание к тому же видосу',
        reply_markup=main_kb(message.from_user.id),
    )
    await s_msg.delete()

    new_video_file = FSInputFile(path=os.path.join(media_dir, 'sample2.mp4'))
    await s_video.edit_media(
        media=InputMediaVideo(
            media=new_video_file,
            caption='Новое видео и у него новое описание.',
        ),
        reply_markup=get_inline_kb(),
    )


@send_files_router.message(Command('send_voice'))
async def send_voice(message: Message, state: FSMContext):
    async with ChatActionSender.record_voice(bot=bot, chat_id=message.from_user.id):
        await asyncio.sleep(2)
        await message.answer_voice(
            voice=FSInputFile(path=os.path.join(media_dir, 'sample-3s.mp3')),
        )


@send_files_router.message(Command('send_video_note'))
async def send_video_note(message: Message, state: FSMContext):
    async with ChatActionSender.record_video_note(bot=bot, chat_id=message.from_user.id):
        await asyncio.sleep(1)
        await message.answer_video_note(
            video_note=FSInputFile(path=os.path.join(media_dir, 'sample2.mp4')),
        )


@send_files_router.message(Command('send_media_group'))
async def send_media_group(message: Message, state: FSMContext):
    photo_1 = InputMediaPhoto(
        type='photo',
        media=FSInputFile(path=os.path.join(media_dir, '1.png')),
        caption='Описание ко <b>ВСЕЙ</b> медиагруппе',
    )
    photo_2 = InputMediaPhoto(
        type='photo',
        media=FSInputFile(path=os.path.join(media_dir, '1.png')),
    )
    photo_3 = InputMediaPhoto(
        type='photo',
        media=FSInputFile(path=os.path.join(media_dir, '1.png')),
    )
    video_1 = InputMediaVideo(
        type='video',
        media=FSInputFile(path=os.path.join(media_dir, 'sample2.mp4')))
    photo_4 = InputMediaPhoto(
        type='photo',
        media=FSInputFile(path=os.path.join(media_dir, '1.png')),
    )
    video_2 = InputMediaVideo(
        type='video',
        media=FSInputFile(path=os.path.join(media_dir, 'sample.mp4')))

    media = [photo_1, photo_2, photo_3, video_1, photo_4, video_2]
    await message.answer_media_group(media=media)
