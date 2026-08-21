        cur.execute("SELECT COUNT(*) FROM users WHERE referred_by=?", (user_id,))
        total_refer = cur.fetchone()[0]
        
        cur.execute("SELECT referral_income FROM users WHERE user_id=?", (user_id,))
        row = cur.fetchone()
        total_refer_income = row[0] if row and row[0] else 0.0
        
        conn.close()

        me = bot.get_me()
        link = f"https://t.me/{me.username}?start={user_id}"
        
        msg = f"""🎁 <b>My Referrals</b>
👤 <b>Total Refer:</b> {total_refer}
😃 <b>Total Refer Income:</b> {total_refer_income:.2f} BDT
🔗 <b>আপনার রেফার লিংক:</b>
<code>{link}</code>

ℹ️ আপনি আপনার প্রতিটি রেফারেলের সম্পূর্ণ করা কাজ থেকে আয়ের 10% কমিশন পাবেন।"""
        bot.send_message(chat_id, msg, reply_markup=main_reply_keyboard())

    elif text == "সাপোর্ট📞":
        msg = """📞 <b>গ্রাহক সেবা কেন্দ্র</b>
━━━━━━━━━━━━━━━━━━━━━━

সম্মানিত মেম্বার,
আপনার যেকোনো সমস্যা বা জিজ্ঞাসার জন্য আমাদের সাপোর্ট টিমের সাথে যোগাযোগ করুন। আমরা দ্রুত সমাধানের চেষ্টা করব।

⚠️ <b>নোট:</b> অযথা মেসেজ দেওয়া থেকে বিরত থাকুন।
ধন্যবাদ!"""
        
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(types.InlineKeyboardButton("💬 সাপোর্ট টিমের সাথে কথা বলুন", url="https://t.me/Jihadfrelancer1"))
        keyboard.add(types.InlineKeyboardButton("📢 আমাদের অফিশিয়াল গ্রুপ", url="https://t.me/crazyteam1123"))
        
        bot.send_message(chat_id, msg, reply_markup=keyboard)

    elif text == "আমি নতুন🥰":
        new_user_msg = """👋 <b>স্বাগতম নতুন মেম্বার!</b>

আমাদের এই বটের মাধ্যমে খুব সহজেই বিভিন্ন সোশ্যাল মিডিয়া ও জিমেইল টাস্ক সম্পন্ন করে আয় করতে পারবেন। 
কাজ শুরু করতে নিচের <b>📖কাজ ▸</b> অপশনে ক্লিক করুন এবং নিয়ম মেনে কাজ জমা দিন। কোনো সমস্যা হলে সাপোর্ট অপশন তো রয়েছেই!"""
        bot.send_message(chat_id, new_user_msg, reply_markup=main_reply_keyboard())

    else:
        bot.send_message(chat_id, "দয়া করে নিচের মেনু থেকে সঠিক অপশনটি বেছে নিন:", reply_markup=main_reply_keyboard())

# ==============================
# CALLBACK HANDLERS
# ==============================
@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id

    if call.data == "ig_click_2fa_btn":
        bot.answer_callback_query(call.id)
        bot.send_message(chat_id, "📥 আপনার <b>2FA Secret Key</b> টি মেসেজ বক্সে পাঠান:")

    elif call.data == "ig_finish":
        if user_id not in user_states or "secret" not in user_states[user_id]:
            bot.answer_callback_query(call.id, "❌ কোনো ২এফএ ডাটা পাওয়া যায়নি!", show_alert=True)
            return

        u_data = user_states[user_id]
        proof = f"IG: {u_data['username']} | Secret: {u_data['secret']}"

        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute("INSERT INTO tasks (user_id, task_type, proof_data, reward) VALUES (?, 'instagram', ?, ?)",
                    (user_id, proof, u_data['reward']))
        conn.commit()
        conn.close()

        delete_credentials_msg(chat_id, user_id)
        bot.answer_callback_query(call.id)
        bot.send_message(chat_id, "🎉 <b>আপনার ইনস্টাগ্রাম টাস্কটি সফলভাবে জমা নেওয়া হয়েছে!</b>", reply_markup=main_reply_keyboard())
        if user_id in user_states:
            del user_states[user_id]

    elif call.data == "fb_click_uid_btn":
        bot.answer_callback_query(call.id)
        bot.send_message(chat_id, "📥 আপনার Facebook <b>UID</b> টি মেসেজ করে পাঠান:")

    elif call.data == "fb_click_cookie_btn":
        bot.answer_callback_query(call.id)
        bot.send_message(chat_id, "📥 এবার অ্যাকাউন্টটির <b>Cookie</b> টি পেস্ট করে পাঠান:")

    elif call.data == "fb_finish":
        if user_id not in user_states or "cookie" not in user_states[user_id]:
            bot.answer_callback_query(call.id, "❌ কোনো তথ্য পাওয়া যায়নি!", show_alert=True)
            return

        u_data = user_states[user_id]
        proof = f"FB Name: {u_data['f_name']} {u_data['l_name']} | UID: {u_data.get('uid')} | Cookie: {u_data['cookie']}"

        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute("INSERT INTO tasks (user_id, task_type, proof_data, reward) VALUES (?, 'facebook', ?, ?)",
                    (user_id, proof, u_data['reward']))
        conn.commit()
        conn.close()

        delete_credentials_msg(chat_id, user_id)
        bot.answer_callback_query(call.id)
        bot.send_message(chat_id, "🎉 <b>ফেসবুক টাস্কটি সফলভাবে জমা নেওয়া হয়েছে!</b>", reply_markup=main_reply_keyboard())
        if user_id in user_states:
            del user_states[user_id]

    elif call.data == "gmail_finish_check":
        if user_id not in user_states or "email" not in user_states[user_id]:
            bot.answer_callback_query(call.id, "❌ টাস্কের ডাটা পাওয়া যায়নি!", show_alert=True)
            return

        email = user_states[user_id]["email"]
        bot.answer_callback_query(call.id, "🔍 জিমেইল অ্যাকাউন্ট ভেরিফাই করা হচ্ছে...", show_alert=False)

        is_created = check_gmail_exists(email)
        if not is_created:
            bot.send_message(chat_id, f"❌ <b>অ্যাপ্রুভ করা সম্ভব হয়নি!</b> ইমেইলটি (<code>{email}</code>) এখনও গুগল সার্ভারে তৈরি করা হয়নি।")
            return

        proof = f"Gmail: {email}"
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute("INSERT INTO tasks (user_id, task_type, proof_data, reward) VALUES (?, 'gmail', ?, ?)",
                    (user_id, proof, user_states[user_id]['reward']))
        conn.commit()
        conn.close()

        delete_credentials_msg(chat_id, user_id)
        bot.send_message(chat_id, "🎉 <b>জিমেইল অ্যাকাউন্টটি সফলভাবে ভেরিফাই হয়ে জমা হয়েছে!</b>", reply_markup=main_reply_keyboard())
        if user_id in user_states:
            del user_states[user_id]

    elif call.data == "cancel_task":
        delete_credentials_msg(chat_id, user_id)
        if user_id in user_states:
            del user_states[user_id]
        bot.answer_callback_query(call.id, "টাস্ক বাতিল করা হয়েছে।")
        bot.send_message(chat_id, "❌ <b>টাস্কটি বাতিল করা হয়েছে।</b>", reply_markup=main_reply_keyboard())

# ==============================
# ADMIN COMMANDS
# ==============================
@bot.message_handler(commands=["admin"])
def admin_panel(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM tasks WHERE status='pending'")
    p_tasks = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM withdrawals WHERE status='pending'")
    p_withdraws = cur.fetchone()[0]
    conn.close()

    msg = f"""
👑 <b>ADMIN PANEL</b>

📌 পেন্ডিং টাস্ক: {p_tasks} টি
📌 পেন্ডিং উইথড্র: {p_withdraws} টি

<b>কমান্ড:</b>
1. টাস্ক দেখতে: `/tasks`
2. টাস্ক অ্যাপ্রুভ: `/approve_t <task_id>`
3. উইথড্র অ্যাপ্রুভ: `/approve_w <withdraw_id>`
"""
    bot.send_message(ADMIN_ID, msg)

@bot.message_handler(commands=["tasks"])
def view_pending_tasks(message):
    if message.from_user.id != ADMIN_ID:
        return

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT id, user_id, task_type, proof_data, reward FROM tasks WHERE status='pending' LIMIT 5")
    rows = cur.fetchall()
    conn.close()

    if not rows:
        bot.send_message(ADMIN_ID, "✅ কোনো পেন্ডিং টাস্ক নেই।")
        return

    for r in rows:
        bot.send_message(
            ADMIN_ID,
            f"🆔 <b>Task #{r[0]}</b>\nUser: <code>{r[1]}</code>\nType: {r[2]}\nReward: {r[4]} BDT\nProof: <code>{r[3]}</code>\n\nঅ্যাপ্রুভ করতে: `/approve_t {r[0]}`"
        )

@bot.message_handler(commands=["approve_t"])
def approve_task_cmd(message):
    if message.from_user.id != ADMIN_ID:
        return

    args = message.text.split()
    if len(args) < 2 or not args[1].isdigit():
        bot.send_message(ADMIN_ID, "উপায়: `/approve_t <task_id>`")
        return

    task_id = int(args[1])
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    
    cur.execute("SELECT user_id, reward, status FROM tasks WHERE id=?", (task_id,))
    task = cur.fetchone()

    if not task or task[2] != 'pending':
        bot.send_message(ADMIN_ID, "❌ টাস্ক পাওয়া যায়নি বা ইতোমধ্যে অ্যাপ্রুভড।")
        conn.close()
        return

    u_id, reward = task[0], task[1]
    cur.execute("UPDATE tasks SET status='approved' WHERE id=?", (task_id,))
    cur.execute("UPDATE users SET balance = balance + ?, total_income = total_income + ? WHERE user_id=?", (reward, reward, u_id))
    
    cur.execute("SELECT referred_by FROM users WHERE user_id=?", (u_id,))
    ref_row = cur.fetchone()
    if ref_row and ref_row[0]:
        ref_id = ref_row[0]
        ref_bonus = reward * 0.10
        cur.execute("UPDATE users SET balance = balance + ?, total_income = total_income + ?, referral_income = referral_income + ? WHERE user_id=?", (ref_bonus, ref_bonus, ref_bonus, ref_id))
        try:
            bot.send_message(ref_id, f"🎉 <b>রেফারেল বোনাস!</b> আপনার ১০% কমিশন (<b>+{ref_bonus:.2f} BDT</b>) যোগ হয়েছে।")
        except Exception:
            pass

    conn.commit()
    conn.close()

    bot.send_message(ADMIN_ID, f"✅ Task #{task_id} Approved!")
    try:
        bot.send_message(u_id, f"🎉 আপনার টাস্ক #{task_id} অ্যাপ্রুভ হয়েছে এবং <b>{reward:.2f} BDT</b> ব্যালেন্সে যোগ হয়েছে!")
    except Exception:
        pass

@bot.message_handler(commands=["approve_w"])
def approve_withdraw_cmd(message):
    if message.from_user.id != ADMIN_ID:
        return

    args = message.text.split()
    if len(args) < 2 or not args[1].isdigit():
        bot.send_message(ADMIN_ID, "উপায়: `/approve_w <withdraw_id>`")
        return

    w_id = int(args[1])
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    
    cur.execute("SELECT user_id, net_amount, method, address, status FROM withdrawals WHERE id=?", (w_id,))
    w_data = cur.fetchone()

    if not w_data or w_data[4] != 'pending':
        bot.send_message(ADMIN_ID, "❌ উইথড্র ডাটা পাওয়া যায়নি বা অ্যাপ্রুভড।")
        conn.close()
        return

    u_id, net_amount, method, address = w_data[0], w_data[1], w_data[2], w_data[3]
    cur.execute("UPDATE withdrawals SET status='approved' WHERE id=?", (w_id,))
    conn.commit()
    conn.close()

    bot.send_message(ADMIN_ID, f"✅ Withdraw #{w_id} Confirmed!")
    try:
        bot.send_message(
            u_id,
            f"🎉 <b>আপনার উইথড্রটি সাকসেস করা হয়েছে!</b>\n\nমাধ্যম: {method}\nআপনার <b>{net_amount:.2f} BDT</b> সফলভাবে পাঠানো হয়েছে:\n📍 <code>{address}</code>"
        )
    except Exception:
        pass

# ==============================
# MAIN LOOP (FLASK + TELEGRAM BOT)
# ==============================
if __name__ == "__main__":
    init_db()
    
    # আলাদা থ্রেডে Flask সার্ভার চালু করা যাতে রেন্ডার কোনো এরর না দেয়
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
    
    print("========================================")
    print("🤖 UPDATED TASK BOT & FLASK ARE RUNNING")
    print("========================================")
    
    while True:
        try:
            bot.infinity_polling(timeout=10, long_polling_timeout=5, skip_pending=True)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)
