Telegram Bot Project
🚀 Quick Run

bash
# Apply database migrations
alembic upgrade head

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
echo "BOT_TOKEN=your_bot_token_here" > .env
echo "ADMIN_ID=your_admin_id_here" >> .env

# Run the bot
cd app
python3 main.py run


