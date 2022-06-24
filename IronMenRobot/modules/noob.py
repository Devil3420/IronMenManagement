import asyncio
from pyrogram import filters
from pyrogram.types import (InlineKeyboardButton,                             InlineKeyboardMarkup, InputMediaPhoto, Message)


from IronMenRobot import pbot as bot
      
Iron_Men = "https://telegra.ph/file/3a5f3eb7a934028c56122.jpg"

@bot.on_message(filters.command(["noob", "owner"]))
async def repo(client, message):   
       await message.reply_photo(      
            photo=Iron_Men,      
            caption=f"""**ʜᴇʏ {message.from_user.mention()},\n\nɪ ᴀᴍ [「 IronMen𒆜 ʀᴏʙᴏᴛ 」](t.me/IronMenRobot)**
""",        
            reply_markup=InlineKeyboardMarkup(   
                  [          
                        [          
                              InlineKeyboardButton("• ᴏᴡɴᴇʀ •", url="https://t.me/always_hungry365"),        
                              
                        ]     
                  ]      
            ),     
      )
      
       
        
         

              
                
                      
                      
                        
                          
             

                                       
                                        
__mod_name__ = "Oᴡɴᴇʀ" 

