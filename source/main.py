from telegram.ext import Application

def main():
	TOKEN = '8087760670:AAFn0pzO8LsttESIZ73W_Aa26TjZGQmq088'
	application = Application.builder().token(TOKEN).concurrent_updates(True).read_timeout(30).write_timeout(30).build()
	print("Telegram Bot started!", flush=True)
	application.run_polling()

if __name__ == '__main__':
	main()