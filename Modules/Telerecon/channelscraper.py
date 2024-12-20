import os
import asyncio
from . import details as ds
import base64
from telethon.sync import TelegramClient, types
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument
import pandas as pd
from colorama import Fore, Style

api_id = ds.apiID
api_hash = ds.apiHash
phone = ds.number


async def scrape_channel_content(channel_name):
    async with TelegramClient(phone, api_id, api_hash) as client:
        try:
            entity = await client.get_entity(channel_name)
            content = []
            post_count = 0

            async for post in client.iter_messages(entity):
                post_count += 1

                text = post.text or ""
                media_base64 = None

                # 미디어 파일 다운로드
                if post.media:
                    if isinstance(post.media, (MessageMediaPhoto, MessageMediaDocument)):
                        try:
                            media_bytes = await client.download_media(
                                message=post,
                                file=bytes
                            ) # media를 다운로드하는 코드해서 바이트 객체로 저장하는 코드.
                            print(f"{Fore.GREEN}Downloaded media.{Style.RESET_ALL}")
                            # 다운로드한 media를 base64로 encode
                            media_base64 = base64.b64encode(media_bytes).decode('utf-8')
                        except Exception as e:
                            print(f"{Fore.RED}Failed to download media: {e}{Style.RESET_ALL}")
                # 메시지 보낸 날짜 및 시간
                message_date = post.date.strftime('%Y-%m-%d %H:%M:%S')  # 'YYYY-MM-DD HH:MM:SS' 포맷으로 저장

                # 기본적으로 모두 값 없음으로 초기화
                username = "N/A"
                first_name = "N/A"
                last_name = "N/A"
                user_id = "N/A"

                if sender := post.sender:
                    if isinstance(sender, types.User):
                        username = sender.username or "N/A"
                        first_name = sender.first_name or "N/A"
                        last_name = sender.last_name if sender.last_name else "N/A"
                        user_id = sender.id

                views = post.views or "N/A"
                message_url = f"https://t.me/{channel_name}/{post.id}"

                content.append({
                    "date": message_date,
                    "text": text,
                    "username": username,
                    "first_name": first_name,
                    "last_name": last_name,
                    "user_id": user_id,
                    "views": views,
                    "url": message_url,
                    "media": media_base64,
                })

                if post_count % 10 == 0:
                    print(
                        f"{Fore.WHITE}{post_count} Posts scraped in {Fore.LIGHTYELLOW_EX}{channel_name}{Style.RESET_ALL}")

            return content

        except Exception as e:
            print(f"An error occurred: {Fore.RED}{e}{Style.RESET_ALL}")
            return []

def main(channel_name):
    # 비동기 데이터 수집 실행
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    content = loop.run_until_complete(scrape_channel_content(channel_name))
    return content

# async def main():
#     try:
#         channel_name = input(
#             f"{Fore.CYAN}Please enter a target Telegram channel (e.g., https://t.me/{Fore.LIGHTYELLOW_EX}your_channel{Style.RESET_ALL}):\n")
#         print(f'You entered "{Fore.LIGHTYELLOW_EX}{channel_name}{Style.RESET_ALL}"')
#         answer = input('Is this correct? (y/n)')
#         if answer != 'y':
#             return
#
#         output_directory = sanitizer.sanitize_filename(f"Collection/{channel_name}")
#         if not os.path.exists(output_directory):
#             os.makedirs(output_directory)
#
#         csv_filename = sanitizer.sanitize_filename(f'{output_directory}/{channel_name}_messages.csv')
#         print(f'Scraping content from {Fore.LIGHTYELLOW_EX}{channel_name}{Style.RESET_ALL}...')
#
#         content = await scrape_channel_content(channel_name)
#
#         if content:
#             df = pd.DataFrame(content, columns=['Datetime', 'Text', 'Username', 'First Name', 'Last Name', 'User ID', 'Views',
#                                                 'Message URL', 'Media File Path'])
#             try:
#                 df.to_csv(csv_filename, index=False)
#                 print(
#                     f'Successfully scraped and saved content to {Fore.LIGHTYELLOW_EX}{csv_filename}{Style.RESET_ALL}.')
#             except Exception as e:
#                 print(f"An error occurred while saving to CSV: {Fore.RED}{e}{Style.RESET_ALL}")
#         else:
#             print(f'{Fore.RED}No content scraped.{Style.RESET_ALL}')
#
#     except Exception as e:
#         print(f"An error occurred: {Fore.RED}{e}{Style.RESET_ALL}")


# if __name__ == '__main__':
#     asyncio.run(main())
