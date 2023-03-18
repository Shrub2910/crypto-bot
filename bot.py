import hikari
import lightbulb
import time
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP as pk
import os
import dotenv

dotenv.load_dotenv()


bot = lightbulb.BotApp(token=os.getenv("TOKEN"), default_enabled_guilds=int(os.getenv("GUILD")))

@bot.command()
@lightbulb.command("rsa", "Creates a public private key pair")
@lightbulb.implements(lightbulb.SlashCommand)
async def pair(ctx: lightbulb.Context) -> None:
    current_time = time.time()

    key = RSA.generate(2048)

    private_key = key.export_key()
    public_key = key.public_key().export_key()

    with open(f"private_{current_time}.pem", "wb") as f:
        f.write(private_key)
    
    with open(f"public_{current_time}.pem", "wb") as f:
        f.write(public_key)
    

    await ctx.respond(attachment=f"public_{current_time}.pem", flags=hikari.MessageFlag(hikari.MessageFlag.EPHEMERAL))
    await ctx.respond(attachment=f"private_{current_time}.pem", flags=hikari.MessageFlag(hikari.MessageFlag.EPHEMERAL))

    os.remove(f"private_{current_time}.pem")
    os.remove(f"public_{current_time}.pem")

@bot.command()
@lightbulb.option("file", "the file to encrypt", type=hikari.Attachment, required=True)
@lightbulb.option("key", "the key to encrypt the file with", type=hikari.Attachment, required=True)
@lightbulb.command("rsaencrypt", "encrypt a file using rsa")
@lightbulb.implements(lightbulb.SlashCommand)
async def rsaencrypt(ctx: lightbulb.Context):
    current_time = time.time()
    file = ctx.options.file
    key = ctx.options.key

    extension = file.filename.split(".")[-1]

    file = await file.read()
    key = await key.read()

    key = RSA.import_key(key)

    cipher = pk.new(key)
    cipher_text = cipher.encrypt(file)

    with open(f"{current_time}.{extension}", "wb") as f:
        f.write(cipher_text)

    await ctx.respond(attachment=f"{current_time}.{extension}", flags=hikari.MessageFlag(hikari.MessageFlag.EPHEMERAL))

    os.remove(f"{current_time}.{extension}")

@bot.command()
@lightbulb.option("file", "the file to decrypt", type=hikari.Attachment, required=True)
@lightbulb.option("key", "the key to decrypt the file with", type=hikari.Attachment, required=True)
@lightbulb.command("rsadecrypt", "decrypt a file using rsa")
@lightbulb.implements(lightbulb.SlashCommand)
async def rsadecrypt(ctx: lightbulb.Context):
    current_time = time.time()
    file = ctx.options.file
    key = ctx.options.key

    extension = file.filename.split(".")[-1]

    file = await file.read()
    key = await key.read()

    key = RSA.import_key(key)

    cipher = pk.new(key)
    plain_text = cipher.decrypt(file)

    with open(f"{current_time}.{extension}", "wb") as f:
        f.write(plain_text)

    await ctx.respond(attachment=f"{current_time}.{extension}", flags=hikari.MessageFlag(hikari.MessageFlag.EPHEMERAL))

    os.remove(f"{current_time}.{extension}")

    
bot.run()



