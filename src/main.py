from core.bot import Gameonix

def main():
    bot : Gameonix = Gameonix()
    bot.run(bot.config.BOT_TOKEN)


if __name__ == "__main__":
    main()
