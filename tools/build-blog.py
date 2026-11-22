#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Builds the EcoBits blog from the shared page shell (faq.html).

Run from the project root:   python3 tools/build-blog.py

Outputs: blog.html (archive), blog-<slug>.html (posts), blog-cat-<slug>.html,
blog-tag-<slug>.html, assets/blog/*.svg (covers) and the "latest posts" block
that is injected into index.html / landing.html between the BLOG markers.
To add a post: append to POSTS below and run again.
"""
import base64, json, os, re, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://ecobits.ir/"          # used for canonical / Open Graph / JSON-LD urls
os.chdir(ROOT)

FA = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")
def fa(n): return str(n).translate(FA)
def esc(s): return html.escape(s, quote=True)

CATS = {
    "kharid":   ("راهنمای خرید", "راهنماهای قدم‌به‌قدم خرید و فروش دارایی دیجیتال با تومان در اکوبیتس."),
    "amoozesh": ("آموزش پایه", "مفاهیم پایه‌ی رمزارز به زبان ساده، برای کسانی که تازه شروع کرده‌اند."),
    "rwa":      ("دارایی‌های واقعی", "هرچه باید درباره‌ی دارایی‌های واقعی توکنیزه‌شده مثل طلا، نقره و نفت دیجیتال بدانید."),
}
TAGS = {
    "tether":       "تتر",
    "stablecoin":   "استیبل‌کوین",
    "bitcoin":      "بیت‌کوین",
    "toman":        "خرید با تومان",
    "risk":         "مدیریت ریسک",
    "tokenization": "توکنیزه‌کردن",
    "xaut":         "تترگلد",
}

POSTS = [
 {
  "slug": "tether-chist", "cat": "kharid", "tags": ["tether", "stablecoin", "toman"],
  "date": "2026-11-21", "fdate": "۳۰ آبان ۱۴۰۵", "cover": "tether",
  "title": "تتر چیست و چطور با تومان تتر بخریم؟",
  "seo_title": "تتر چیست؟ راهنمای خرید تتر با تومان | بلاگ اکوبیتس",
  "desc": "تتر (USDT) چیست، چرا قیمتش به دلار وابسته است و چطور می‌شود آن را با تومان خرید؟ راهنمای ساده‌ی خرید تتر، ریسک‌ها و نکته‌های پیش از خرید.",
  "excerpt": "تتر پرمعامله‌ترین استیبل‌کوین دنیاست. در این راهنما می‌خوانید تتر چیست، قیمتش از کجا می‌آید و خرید آن با تومان چه مراحلی دارد.",
  "alt": "سکه‌ی تتر در کنار یک کارت بانکی، نماد خرید تتر با تومان",
  "cta": ("coin-usdt.html", "قیمت و خرید تتر"),
  "tldr": ["تتر (USDT) یک استیبل‌کوین است که برای هم‌قیمت‌ماندن با دلار آمریکا طراحی شده.",
           "قیمت تومانی تتر با نرخ دلار در بازار بالا و پایین می‌رود.",
           "در اکوبیتس تتر را با تومان و از حساب بانکی خودتان می‌خرید و کارمزد را پیش از تأیید می‌بینید."],
  "body": """
<p>اگر تازه با دنیای رمزارز آشنا شده باشید، احتمالاً اولین اسمی که شنیده‌اید «تتر» است. خیلی‌ها خرید دارایی دیجیتال را با تتر شروع می‌کنند، چون قیمتش مثل بیت‌کوین هر روز چند درصد جابه‌جا نمی‌شود. در این مطلب به زبان ساده می‌گوییم تتر چیست، چه فرقی با بقیه‌ی رمزارزها دارد و <strong>خرید تتر با تومان</strong> چطور انجام می‌شود.</p>

<h2>تتر چیست؟</h2>
<p>تتر با نماد <strong>USDT</strong> یک «استیبل‌کوین» است؛ یعنی رمزارزی که قرار است قیمتش ثابت بماند. هر واحد تتر برای برابری با یک دلار آمریکا طراحی شده و شرکت منتشرکننده‌ی آن اعلام می‌کند در برابر تترهای در گردش، ذخیره نگه می‌دارد. تتر از سال ۲۰۱۴ در بازار است و روی چند شبکه‌ی بلاک‌چین مختلف منتشر می‌شود.</p>
<p>به همین دلیل، تتر در عمل نقش «دلار دیجیتال» را در بازار رمزارز بازی می‌کند: معامله‌گرها از آن برای نگه‌داشتن ارزش دارایی‌شان بین دو معامله استفاده می‌کنند و بخش بزرگی از خرید و فروش رمزارزها در دنیا با تتر انجام می‌شود.</p>

<h2>قیمت تتر به تومان از کجا می‌آید؟</h2>
<p>چون هر تتر حدوداً یک دلار می‌ارزد، <strong>قیمت تتر به تومان</strong> هم تقریباً همان نرخ دلار در بازار است. اگر نرخ دلار بالا برود، قیمت تومانی تتر هم بالا می‌رود و برعکس. تفاوت‌های کوچک بین قیمت تتر در صرافی‌های مختلف معمولاً به عرضه و تقاضای همان لحظه برمی‌گردد.</p>
<div class="note">تتر «بدون ریسک» نیست. ثبات آن نسبت به دلار است، نه نسبت به تومان. پس اگر نرخ دلار پایین بیاید، ارزش تومانی تتر شما هم کم می‌شود.</div>

<h2>تتر چه فرقی با بیت‌کوین دارد؟</h2>
<div class="tblwrap"><table>
<thead><tr><th>ویژگی</th><th>تتر (USDT)</th><th>بیت‌کوین (BTC)</th></tr></thead>
<tbody>
<tr><td>هدف</td><td>حفظ ارزش برابر با دلار</td><td>دارایی کمیاب با عرضه‌ی محدود</td></tr>
<tr><td>نوسان قیمت دلاری</td><td>بسیار کم</td><td>زیاد</td></tr>
<tr><td>منتشرکننده</td><td>یک شرکت مشخص</td><td>شبکه‌ی غیرمتمرکز</td></tr>
<tr><td>کاربرد رایج</td><td>نگهداری ارزش و معامله</td><td>سرمایه‌گذاری بلندمدت</td></tr>
</tbody></table></div>
<p>اگر می‌خواهید بیشتر درباره‌ی بیت‌کوین بدانید، <a href="blog-kharid-bitcoin.html">راهنمای خرید بیت‌کوین برای تازه‌کارها</a> را بخوانید.</p>

<h2>مراحل خرید تتر با تومان در اکوبیتس</h2>
<ol>
<li><strong>حساب بسازید.</strong> با شماره موبایل ثبت‌نام می‌کنید و کد تأیید برایتان پیامک می‌شود.</li>
<li><strong>تومان واریز کنید.</strong> واریز از حساب بانکی خودتان و به تومان انجام می‌شود. به کیف‌پول یا آدرس نیازی ندارید.</li>
<li><strong>مبلغ را وارد کنید.</strong> در <a href="coin-usdt.html">صفحه‌ی تتر</a> مبلغ تومانی را می‌نویسید و مقدار تتری را که می‌گیرید همان لحظه می‌بینید.</li>
<li><strong>کارمزد را ببینید و تأیید کنید.</strong> قیمت و کارمزد پیش از تأیید نهایی نمایش داده می‌شود.</li>
</ol>
<p>هر وقت خواستید می‌توانید تتر را بفروشید و تومان را به همان حساب بانکی برداشت کنید. مراحل کامل را در بخش <a href="landing.html#steps">چهار قدم تا برداشت</a> ببینید.</p>

<h2>پیش از خرید تتر به چه نکته‌هایی توجه کنیم؟</h2>
<ul>
<li><strong>هدفتان را مشخص کنید.</strong> تتر برای حفظ ارزش در برابر دلار مناسب است، نه برای رشد قیمت دلاری.</li>
<li><strong>قیمت نهایی را نگاه کنید.</strong> مبلغی که در نهایت می‌پردازید، قیمت واحد به‌علاوه‌ی کارمزد است.</li>
<li><strong>ریسک منتشرکننده را بشناسید.</strong> ثبات تتر به ذخایر و عملکرد شرکت منتشرکننده وابسته است.</li>
<li><strong>با مبلغی شروع کنید که با آن راحتید.</strong> هیچ سرمایه‌گذاری‌ای سود تضمین‌شده ندارد.</li>
</ul>
""",
  "faq": [
    ("آیا قیمت تتر همیشه یک دلار است؟", "تتر برای برابری با یک دلار طراحی شده و معمولاً خیلی نزدیک به آن معامله می‌شود، اما تضمینی وجود ندارد و در مقاطعی کمی بالاتر یا پایین‌تر از یک دلار قیمت خورده است."),
    ("برای خرید تتر به کیف‌پول نیاز دارم؟", "در اکوبیتس نه. تتر در حساب کاربری خودتان نگهداری می‌شود و خرید و فروش آن فقط با تومان و از مسیر حساب بانکی انجام می‌گیرد."),
    ("کارمزد خرید تتر چقدر است؟", "کارمزد هر سفارش پیش از تأیید نهایی در همان صفحه نمایش داده می‌شود تا مبلغ دقیق را قبل از پرداخت بدانید."),
  ],
 },
 {
  "slug": "kharid-bitcoin", "cat": "amoozesh", "tags": ["bitcoin", "toman", "risk"],
  "date": "2026-11-17", "fdate": "۲۶ آبان ۱۴۰۵", "cover": "bitcoin",
  "title": "راهنمای خرید بیت‌کوین برای تازه‌کارها",
  "seo_title": "راهنمای خرید بیت‌کوین با تومان برای تازه‌کارها | بلاگ اکوبیتس",
  "desc": "بیت‌کوین چیست و اولین خرید را چطور انجام دهیم؟ راهنمای ساده‌ی خرید بیت‌کوین با تومان، خرید کسری از بیت‌کوین و اشتباه‌های رایج تازه‌کارها.",
  "excerpt": "لازم نیست یک بیت‌کوین کامل بخرید. در این راهنما با مفاهیم پایه، روش خرید بیت‌کوین با تومان و اشتباه‌های رایج تازه‌کارها آشنا می‌شوید.",
  "alt": "سکه‌ی بیت‌کوین روی نمودار صعودی قیمت",
  "cta": ("coin-btc.html", "قیمت و خرید بیت‌کوین"),
  "tldr": ["بیت‌کوین اولین رمزارز دنیاست و تعداد کل آن به ۲۱ میلیون واحد محدود است.",
           "می‌توانید کسری از یک بیت‌کوین را بخرید؛ خرید با مبلغ کم هم ممکن است.",
           "قیمت بیت‌کوین نوسان زیادی دارد؛ فقط پولی را وارد کنید که به آن نیاز فوری ندارید."],
  "body": """
<p>بیت‌کوین معروف‌ترین رمزارز دنیاست و خیلی‌ها خرید دارایی دیجیتال را با آن شروع می‌کنند. اما قیمت بالای هر واحد و نوسان‌های شدیدش ممکن است تازه‌کارها را سردرگم کند. این راهنما برای کسانی است که می‌خواهند <strong>اولین خرید بیت‌کوین</strong> خود را آگاهانه و بدون عجله انجام دهند.</p>

<h2>بیت‌کوین چیست؟</h2>
<p>بیت‌کوین با نماد <strong>BTC</strong> اولین رمزارز جهان است که در سال ۲۰۰۹ معرفی شد. هیچ بانک یا دولتی آن را منتشر نمی‌کند؛ شبکه‌ای از رایانه‌ها در سراسر دنیا تراکنش‌ها را ثبت و تأیید می‌کنند. تعداد کل بیت‌کوین‌ها به <strong>۲۱ میلیون واحد</strong> محدود است و همین کمیابی یکی از دلایلی است که بسیاری آن را با طلا مقایسه می‌کنند.</p>

<h2>آیا باید یک بیت‌کوین کامل بخریم؟</h2>
<p>نه. هر بیت‌کوین تا هشت رقم اعشار قابل تقسیم است و می‌توانید هر کسری از آن را بخرید. یعنی به‌جای فکرکردن به قیمت یک واحد کامل، کافی است مبلغ تومانی مورد نظرتان را مشخص کنید؛ مقدار بیت‌کوینی که می‌گیرید متناسب با همان مبلغ حساب می‌شود.</p>

<h2>مراحل خرید بیت‌کوین با تومان</h2>
<ol>
<li><strong>ثبت‌نام کنید.</strong> ساخت حساب در اکوبیتس با شماره موبایل انجام می‌شود.</li>
<li><strong>تومان واریز کنید.</strong> واریز از حساب بانکی خودتان است و به کیف‌پول شخصی نیاز ندارید.</li>
<li><strong>مبلغ خرید را وارد کنید.</strong> در <a href="coin-btc.html">صفحه‌ی بیت‌کوین</a> مبلغ تومانی را بنویسید تا مقدار دقیق بیت‌کوین را ببینید.</li>
<li><strong>پیش از تأیید، قیمت و کارمزد را مرور کنید.</strong> بعد از تأیید، بیت‌کوین به حساب شما اضافه می‌شود.</li>
</ol>
<div class="note">در اکوبیتس ورود و خروج پول فقط تومانی و از مسیر بانکی است. دارایی در حساب کاربری شما می‌ماند و هر وقت خواستید آن را می‌فروشید و تومان برداشت می‌کنید.</div>

<h2>قیمت بیت‌کوین چرا این‌قدر بالا و پایین می‌رود؟</h2>
<p>قیمت بیت‌کوین را عرضه و تقاضا در بازار جهانی تعیین می‌کند. اخبار اقتصادی، تصمیم‌های قانون‌گذاران و رفتار سرمایه‌گذاران بزرگ می‌تواند در مدت کوتاهی قیمت را چند درصد جابه‌جا کند. برای خریدار ایرانی یک عامل دیگر هم هست: <strong>قیمت بیت‌کوین به تومان</strong> علاوه بر قیمت جهانی، به نرخ دلار هم وابسته است.</p>

<h2>پنج اشتباه رایج تازه‌کارها</h2>
<ul>
<li><strong>خرید با هیجان.</strong> خرید در اوج هیجان بازار و فروش در اولین افت، رایج‌ترین دلیل ضرر است.</li>
<li><strong>واردکردن پولی که لازم دارید.</strong> فقط با مبلغی وارد شوید که در کوتاه‌مدت به آن نیاز ندارید.</li>
<li><strong>گذاشتن همه‌ی سرمایه روی یک دارایی.</strong> تقسیم سرمایه ریسک را کم می‌کند. برای بخشی که می‌خواهید کم‌نوسان بماند، می‌توانید <a href="blog-tether-chist.html">تتر</a> را بررسی کنید.</li>
<li><strong>نگاه‌نکردن به کارمزد.</strong> مبلغ نهایی را همیشه پیش از تأیید ببینید.</li>
<li><strong>اعتماد به وعده‌ی سود قطعی.</strong> هیچ‌کس نمی‌تواند سود بیت‌کوین را تضمین کند.</li>
</ul>

<h2>خرید یک‌جا بهتر است یا پله‌ای؟</h2>
<p>بعضی‌ها به‌جای اینکه کل مبلغ را یک‌جا خرید کنند، آن را به چند بخش تقسیم می‌کنند و در فاصله‌های زمانی مشخص می‌خرند. این روش که به «خرید پله‌ای» معروف است، اثر نوسان‌های کوتاه‌مدت را روی قیمت میانگین خرید کمتر می‌کند. این یک توصیه‌ی سرمایه‌گذاری نیست؛ فقط یکی از روش‌هایی است که خریداران برای مدیریت ریسک به کار می‌برند.</p>
""",
  "faq": [
    ("با چه مبلغی می‌شود بیت‌کوین خرید؟", "لازم نیست یک بیت‌کوین کامل بخرید. مبلغ تومانی را وارد می‌کنید و کسری از بیت‌کوین متناسب با همان مبلغ می‌گیرید."),
    ("آیا خرید بیت‌کوین سود تضمینی دارد؟", "خیر. قیمت بیت‌کوین نوسان زیادی دارد و ممکن است ارزش دارایی شما کم یا زیاد شود. اکوبیتس هیچ سود یا اصل سرمایه‌ای را تضمین نمی‌کند."),
    ("بیت‌کوینی که می‌خرم کجا نگهداری می‌شود؟", "دارایی در حساب کاربری شما در اکوبیتس نگهداری می‌شود و هر زمان بخواهید می‌توانید آن را بفروشید و تومان را به حساب بانکی خودتان برداشت کنید."),
  ],
 },
 {
  "slug": "rwa-chist", "cat": "rwa", "tags": ["tokenization", "xaut", "risk"],
  "date": "2026-11-12", "fdate": "۲۱ آبان ۱۴۰۵", "cover": "rwa",
  "title": "دارایی‌های واقعی توکنیزه‌شده (RWA) چیست؟",
  "seo_title": "RWA چیست؟ دارایی‌های واقعی توکنیزه‌شده، از طلا تا نفت دیجیتال | بلاگ اکوبیتس",
  "desc": "RWA یا دارایی واقعی توکنیزه‌شده چیست و طلا، نقره و نفت دیجیتال چطور کار می‌کنند؟ مزایا، ریسک‌ها و تفاوت آن با رمزارزهای معمول به زبان ساده.",
  "excerpt": "طلا، نقره و نفت هم می‌توانند به شکل توکن دیجیتال معامله شوند. در این مطلب می‌خوانید RWA چیست، چه مزایا و ریسک‌هایی دارد و تترگلد چگونه کار می‌کند.",
  "alt": "شمش‌های طلا در کنار سکه‌ی تترگلد، نماد دارایی‌های واقعی توکنیزه‌شده",
  "cta": ("coin-xaut.html", "صفحه‌ی تترگلد"),
  "tldr": ["RWA یعنی دارایی‌ای در دنیای واقعی (مثل طلا یا نفت) که نماینده‌ی دیجیتالش به شکل توکن معامله می‌شود.",
           "ارزش این توکن‌ها از دارایی پشتوانه می‌آید، نه فقط از عرضه و تقاضای خود توکن.",
           "دارایی‌های واقعی هنوز در اکوبیتس فعال نیستند و فعلاً فقط قیمت و اطلاعاتشان نمایش داده می‌شود."],
  "body": """
<p>تا چند سال پیش، دارایی دیجیتال فقط به معنی رمزارزهایی مثل بیت‌کوین و اتریوم بود. اما حالا بخش تازه‌ای در این بازار شکل گرفته که دارایی‌های آشنای دنیای واقعی را به شکل توکن عرضه می‌کند. به این دسته <strong>RWA</strong> یا «دارایی‌های واقعی توکنیزه‌شده» می‌گویند.</p>

<h2>RWA یعنی چه؟</h2>
<p>RWA کوتاه‌شده‌ی عبارت Real World Assets است، یعنی «دارایی‌های دنیای واقعی». در این مدل، یک دارایی فیزیکی یا مالی مثل طلا، نقره، نفت یا سهام نزد یک نهاد نگهداری می‌شود و در برابر آن، توکن‌هایی روی بلاک‌چین منتشر می‌شود. هر توکن نماینده‌ی بخشی از همان دارایی است. به این فرایند <strong>توکنیزه‌کردن</strong> می‌گویند.</p>

<h2>توکنیزه‌شدن چطور کار می‌کند؟</h2>
<ol>
<li><strong>نگهداری دارایی.</strong> دارایی واقعی، مثلاً شمش طلا، نزد یک امین یا خزانه نگهداری می‌شود.</li>
<li><strong>انتشار توکن.</strong> ناشر به اندازه‌ی دارایی نگهداری‌شده توکن منتشر می‌کند.</li>
<li><strong>معامله.</strong> توکن‌ها مثل هر دارایی دیجیتال دیگری خرید و فروش می‌شوند و قیمتشان قیمت دارایی پشتوانه را دنبال می‌کند.</li>
</ol>

<h2>نمونه‌های رایج دارایی‌های واقعی</h2>
<div class="tblwrap"><table>
<thead><tr><th>دارایی</th><th>پشتوانه</th><th>قیمت از چه چیزی اثر می‌گیرد؟</th></tr></thead>
<tbody>
<tr><td><a href="coin-xaut.html">تترگلد (XAUT)</a></td><td>طلای فیزیکی</td><td>قیمت جهانی طلا</td></tr>
<tr><td><a href="coin-slvon.html">نقره دیجیتال</a></td><td>نقره</td><td>قیمت جهانی نقره و تقاضای صنعتی</td></tr>
<tr><td><a href="coin-copxon.html">مس دیجیتال</a></td><td>مس</td><td>رشد صنعت و ساخت‌وساز</td></tr>
<tr><td><a href="coin-usoon.html">نفت دیجیتال</a></td><td>نفت</td><td>عرضه و تقاضای جهانی انرژی</td></tr>
</tbody></table></div>
<p>برای نمونه، ناشر تترگلد اعلام می‌کند هر توکن XAUT نماینده‌ی یک اونس طلای فیزیکی است که در خزانه نگهداری می‌شود. بنابراین قیمت آن به قیمت جهانی طلا گره خورده است.</p>

<h2>مزایای دارایی‌های توکنیزه‌شده</h2>
<ul>
<li><strong>خرید خُرد.</strong> می‌شود کسری از یک دارایی گران را خرید، بدون نیاز به خرید یک شمش یا یک قرارداد کامل.</li>
<li><strong>دسترسی ساده‌تر.</strong> درگیر انبارداری، حمل یا قراردادهای پیچیده نمی‌شوید.</li>
<li><strong>تنوع سبد.</strong> قیمت طلا یا نفت لزوماً هم‌جهت با بیت‌کوین حرکت نمی‌کند و می‌تواند به تنوع دارایی‌ها کمک کند.</li>
</ul>

<h2>ریسک‌هایی که باید بدانید</h2>
<ul>
<li><strong>ریسک ناشر و امین.</strong> ارزش توکن به این وابسته است که دارایی پشتوانه واقعاً وجود داشته باشد و درست نگهداری شود.</li>
<li><strong>ریسک قیمت.</strong> طلا، نقره و نفت هم نوسان دارند؛ توکنیزه‌شدن نوسان را از بین نمی‌برد.</li>
<li><strong>ریسک نرخ ارز.</strong> قیمت تومانی این دارایی‌ها علاوه بر قیمت جهانی، به نرخ دلار هم وابسته است.</li>
<li><strong>ریسک قانونی.</strong> قوانین مربوط به دارایی‌های توکنیزه‌شده در کشورهای مختلف در حال تغییر است.</li>
</ul>
<div class="note">دارایی‌های واقعی هنوز در اکوبیتس قابل خرید و فروش نیستند. مشخصات ناشر، پشتوانه و کارمزد هر دارایی پیش از فعال‌شدن در صفحه‌ی همان دارایی منتشر می‌شود.</div>

<h2>RWA چه فرقی با رمزارزهای معمول دارد؟</h2>
<p>ارزش بیت‌کوین از کمیابی و تقاضای خودش می‌آید و پشتوانه‌ی فیزیکی ندارد. <a href="blog-tether-chist.html">تتر</a> به دلار وابسته است. اما یک توکن RWA نماینده‌ی دارایی‌ای بیرون از بلاک‌چین است و رفتارش را همان دارایی تعیین می‌کند. اگر با مفاهیم پایه آشنا نیستید، خواندن <a href="blog-kharid-bitcoin.html">راهنمای خرید بیت‌کوین</a> شروع خوبی است.</p>
""",
  "faq": [
    ("RWA مخفف چیست؟", "RWA مخفف Real World Assets به معنی دارایی‌های دنیای واقعی است؛ دارایی‌هایی مثل طلا، نقره یا نفت که نماینده‌ی دیجیتال آن‌ها به شکل توکن معامله می‌شود."),
    ("آیا تترگلد همان طلاست؟", "تترگلد توکنی است که به گفته‌ی ناشرش پشتوانه‌ی طلای فیزیکی دارد و قیمتش قیمت جهانی طلا را دنبال می‌کند. خود توکن یک دارایی دیجیتال است و ریسک ناشر را هم به همراه دارد."),
    ("می‌توانم الان در اکوبیتس دارایی واقعی بخرم؟", "هنوز نه. در حال حاضر تتر، بیت‌کوین و اتریوم قابل خرید و فروش‌اند و دارایی‌های واقعی با برچسب «به‌زودی» نمایش داده می‌شوند."),
  ],
 },
]
for p in POSTS:
    p["file"] = "blog-%s.html" % p["slug"]
    words = len(re.sub(r"<[^>]+>", " ", p["body"]).split())
    p["mins"] = max(2, round(words / 190))
POSTS.sort(key=lambda p: p["date"], reverse=True)

# ---------------------------------------------------------------- covers
def b64(name):
    return "data:image/webp;base64," + base64.b64encode(open("assets/coins/%s.webp" % name, "rb").read()).decode()

def cover_tether():
    rings = "".join('<circle cx="840" cy="315" r="%d" fill="none" stroke="#7fbfee" stroke-opacity="%.2f" stroke-width="1.5"/>' % (r, o)
                    for r, o in [(170, .55), (250, .4), (330, .28), (410, .18)])
    dots = "".join('<circle cx="%d" cy="%d" r="%d" fill="#0f9df5" fill-opacity="%.2f"/>' % d
                   for d in [(470, 330, 7, .9), (510, 322, 6, .7), (548, 316, 5, .5), (584, 312, 4, .35)])
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" role="img">
<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f1f9ff"/><stop offset="1" stop-color="#c9e6ff"/></linearGradient>
<linearGradient id="card" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0b5fa8"/><stop offset=".55" stop-color="#0f9df5"/><stop offset="1" stop-color="#1eb0d4"/></linearGradient>
<linearGradient id="chip" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffe7a8"/><stop offset="1" stop-color="#d9a94a"/></linearGradient>
<radialGradient id="glow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#ffffff" stop-opacity=".9"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/></radialGradient></defs>
<rect width="1200" height="630" fill="url(#bg)"/>
<g stroke="#9fcdf0" stroke-opacity=".5" stroke-width="1">''' + "".join('<path d="M%d 630 L%d 470"/>' % (x, 600 + (x - 600) * 0.45) for x in range(-300, 1501, 120)) + \
    "".join('<path d="M0 %d H1200"/>' % y for y in (486, 512, 548, 596)) + '''</g>
''' + rings + '''
<circle cx="840" cy="315" r="230" fill="url(#glow)"/>
<g transform="translate(140 196) rotate(-7 170 108)">
<rect x="10" y="16" width="340" height="216" rx="26" fill="#0a3f73" fill-opacity=".22"/>
<rect width="340" height="216" rx="26" fill="url(#card)"/>
<rect x="30" y="34" width="58" height="42" rx="9" fill="url(#chip)"/>
<g fill="#cfeaff"><rect x="30" y="118" width="56" height="10" rx="5"/><rect x="100" y="118" width="56" height="10" rx="5"/><rect x="170" y="118" width="56" height="10" rx="5"/><rect x="240" y="118" width="56" height="10" rx="5"/></g>
<rect x="30" y="162" width="120" height="10" rx="5" fill="#9fd4f7"/>
<circle cx="286" cy="172" r="20" fill="#ffffff" fill-opacity=".35"/><circle cx="262" cy="172" r="20" fill="#ffffff" fill-opacity=".55"/>
</g>
''' + dots + '''
<image href="''' + b64("usdt") + '''" x="640" y="115" width="400" height="400"/>
<image href="''' + b64("usdt") + '''" x="1040" y="70" width="110" height="110" opacity=".55"/>
<image href="''' + b64("usdt") + '''" x="560" y="470" width="84" height="84" opacity=".45"/>
</svg>'''

def cover_bitcoin():
    pts = [(60, 520), (170, 500), (260, 470), (350, 485), (440, 420), (530, 440), (620, 360), (710, 380), (800, 290)]
    d = "M%d %d" % pts[0]
    for i in range(len(pts) - 1):
        p0 = pts[i - 1] if i else pts[0]; p1 = pts[i]; p2 = pts[i + 1]; p3 = pts[i + 2] if i + 2 < len(pts) else pts[-1]
        d += " C%.0f %.0f %.0f %.0f %d %d" % (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6,
                                              p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6, p2[0], p2[1])
    grid = "".join('<path d="M0 %d H1200"/>' % y for y in range(90, 631, 90)) + "".join('<path d="M%d 0 V630"/>' % x for x in range(100, 1201, 100))
    bars = "".join('<rect x="%d" y="%d" width="34" height="%d" rx="6" fill="#1f5c8f" fill-opacity=".55"/>' % (x, 630 - h, h)
                   for x, h in [(80, 60), (170, 90), (260, 70), (350, 120), (440, 100), (530, 150), (620, 130), (710, 190)])
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" role="img">
<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#06162a"/><stop offset="1" stop-color="#0d3a63"/></linearGradient>
<linearGradient id="ln" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#0f9df5"/><stop offset=".6" stop-color="#1eb0d4"/><stop offset="1" stop-color="#4dea72"/></linearGradient>
<linearGradient id="ar" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1eb0d4" stop-opacity=".42"/><stop offset="1" stop-color="#1eb0d4" stop-opacity="0"/></linearGradient>
<radialGradient id="glow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#f7a53a" stop-opacity=".5"/><stop offset="1" stop-color="#f7a53a" stop-opacity="0"/></radialGradient></defs>
<rect width="1200" height="630" fill="url(#bg)"/>
<g stroke="#ffffff" stroke-opacity=".06" stroke-width="1">''' + grid + '''</g>
''' + bars + '''
<path d="''' + d + ''' L800 630 L60 630 Z" fill="url(#ar)"/>
<path d="''' + d + '''" fill="none" stroke="url(#ln)" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
<circle cx="800" cy="290" r="26" fill="#4dea72" fill-opacity=".22"/><circle cx="800" cy="290" r="11" fill="#4dea72"/>
<circle cx="930" cy="290" r="260" fill="url(#glow)"/>
<image href="''' + b64("btc") + '''" x="720" y="80" width="430" height="430"/>
<image href="''' + b64("btc") + '''" x="90" y="70" width="110" height="110" opacity=".4"/>
</svg>'''

def cover_rwa():
    def bar(x, y, s=1.0):
        w, h, dx, dy = 210 * s, 62 * s, 46 * s, 30 * s
        return ('<g><path d="M%.0f %.0f l%.0f %.0f h%.0f l%.0f %.0f Z" fill="#f6d57a"/>'
                '<path d="M%.0f %.0f h%.0f l%.0f %.0f h%.0f Z" fill="#d9a441"/>'
                '<path d="M%.0f %.0f l%.0f %.0f l%.0f %.0f l%.0f %.0f Z" fill="#b88326"/></g>') % (
            x + dx * .4, y, -dx * .4, dy, w, -dx * .4, -dy,
            x, y + dy, w, dx * .25, h, -(w + dx * .5),
            x + w - dx * .0, y + dy, dx * .25, h, dx * .5, -dy * .8, -dx * .35, -h * .6)
    hexes = ""
    for i, (cx, cy) in enumerate([(360, 150), (450, 150), (405, 228), (495, 228), (540, 150)]):
        pts = " ".join("%.0f,%.0f" % (cx + 44 * __import__("math").cos(__import__("math").radians(60 * k + 30)),
                                       cy + 44 * __import__("math").sin(__import__("math").radians(60 * k + 30))) for k in range(6))
        hexes += '<polygon points="%s" fill="#ffffff" fill-opacity="%.2f" stroke="#30c6ae" stroke-opacity=".7" stroke-width="2"/>' % (pts, .7 - i * .09)
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" role="img">
<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f1fbf7"/><stop offset=".6" stop-color="#d6f1ea"/><stop offset="1" stop-color="#c2e6f3"/></linearGradient>
<radialGradient id="glow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#ffffff" stop-opacity=".95"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/></radialGradient></defs>
<rect width="1200" height="630" fill="url(#bg)"/>
<g stroke="#8fd3c4" stroke-opacity=".45" stroke-width="1">''' + "".join('<path d="M%d 630 L%d 440"/>' % (x, 600 + (x - 600) * 0.4) for x in range(-300, 1501, 120)) + \
    "".join('<path d="M0 %d H1200"/>' % y for y in (458, 486, 526, 582)) + '''</g>
''' + hexes + '''
<path d="M560 190 C640 190 660 250 720 270" fill="none" stroke="#30c6ae" stroke-width="3" stroke-dasharray="3 12" stroke-linecap="round"/>
<ellipse cx="330" cy="520" rx="300" ry="34" fill="#0b5f58" fill-opacity=".12"/>
''' + bar(110, 420) + bar(300, 420) + bar(205, 345) + '''
<circle cx="880" cy="320" r="250" fill="url(#glow)"/>
<image href="''' + b64("xaut") + '''" x="680" y="110" width="410" height="410"/>
<image href="''' + b64("xaut") + '''" x="1050" y="430" width="100" height="100" opacity=".5"/>
</svg>'''

os.makedirs("assets/blog", exist_ok=True)
for name, fn in (("tether", cover_tether), ("bitcoin", cover_bitcoin), ("rwa", cover_rwa)):
    open("assets/blog/%s.svg" % name, "w", encoding="utf8").write(fn())

# ---------------------------------------------------------------- shell
shell = open("faq.html", encoding="utf8").read()
s_style0 = shell.index("<style>"); s_style1 = shell.index("</style>")
STYLE = shell[s_style0:s_style1]
PRE = shell[s_style1:shell.index("<main>")]
SIGNUP = shell[shell.index('  <section class="signup" id="signup">'):shell.index("</main>")]
after = shell[shell.index("</main>"):]
POST = after[:after.index('<script id="faqData"')] + after[after.index("<script>\n/* the sign-up panel"):]
_b0 = POST.index('<nav class="bbar"'); _b1 = POST.index("</nav>", _b0)
POST = POST[:_b0] + POST[_b0:_b1].replace(' aria-current="page"', "") + POST[_b1:]   # the shell is the FAQ page: drop its active tab

MARK = "  /* dropdown rows: a bar on the leading"
CARD_CSS = '''  /* ============ BLOG: post cards (shared by the blog and the home page) ============ */
  .pgrid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 22px; }
  .pcard {
    position: relative; display: flex; flex-direction: column; overflow: hidden; border-radius: var(--r-lg);
    background: var(--surface); border: 1px solid var(--line-soft); box-shadow: var(--sh-1);
    transition: transform 0.3s var(--ease), box-shadow 0.3s var(--ease), border-color 0.26s;
  }
  .pcard:hover { transform: translateY(-5px); box-shadow: var(--sh-2); border-color: var(--line); }
  .pcard .cv { display: block; aspect-ratio: 1200 / 630; overflow: hidden; background: var(--bg-2); }
  .pcard .cv img { display: block; width: 100%; height: 100%; object-fit: cover; transition: transform 0.6s var(--ease); }
  .pcard:hover .cv img { transform: scale(1.04); }
  .pcard .bd { flex: 1; display: flex; flex-direction: column; gap: 10px; padding: 18px 20px 20px; }
  .pcat {
    position: relative; z-index: 1; align-self: flex-start; font-size: 0.72rem; --fw: 620; font-weight: var(--fw);
    padding: 4px 11px; border-radius: 999px; background: var(--tint); color: var(--blue-700);
  }
  .pcard h3 { font-size: 1.04rem; --fw: 700; font-weight: var(--fw); line-height: 1.75; color: var(--ink-900); }
  .pcard h3 a::after { content: ""; position: absolute; inset: 0; }
  .pcard p { font-size: 0.86rem; color: var(--ink-500); line-height: 1.95; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
  .pmeta { margin-top: auto; padding-top: 4px; display: flex; align-items: center; gap: 9px; font-size: 0.76rem; color: var(--ink-400); }
  .pmeta i { width: 3px; height: 3px; border-radius: 50%; background: var(--ink-300); }
  @media (max-width: 1000px) { .pgrid { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
  @media (max-width: 620px) {
    .pgrid.swipe {
      display: flex; gap: 12px; overflow-x: auto; scroll-snap-type: x mandatory; -webkit-overflow-scrolling: touch;
      margin-inline: -20px; padding: 6px 20px 22px; scroll-padding-inline: 20px; scrollbar-width: none;
    }
    .pgrid.swipe::-webkit-scrollbar { display: none; }
    .pgrid.swipe > * { flex: 0 0 82%; scroll-snap-align: start; }
    .pgrid:not(.swipe) { grid-template-columns: 1fr; }
  }

'''
BLOG_CSS = CARD_CSS + '''  /* ============ BLOG: archive, taxonomy and post pages ============ */
  .blog-cats { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 26px; }
  .bchip {
    display: inline-flex; align-items: center; gap: 7px; padding: 8px 16px; border-radius: 999px;
    border: 1.5px solid var(--line); background: var(--surface); color: var(--ink-700);
    font-size: 0.84rem; --fw: 580; font-weight: var(--fw); transition: border-color 0.22s, color 0.22s, background 0.22s;
  }
  .bchip:hover { border-color: var(--blue); color: var(--blue-700); }
  .bchip .n { font-size: 0.72rem; color: var(--ink-400); }
  .bchip[aria-current="page"] { background: var(--blue); border-color: var(--blue); color: #fff; }
  .bchip[aria-current="page"] .n { color: #d8efff; }
  .bsec { padding-block: 52px; }
  .bsec + .bsec { padding-top: 0; }
  .bsec-h { display: flex; align-items: baseline; justify-content: space-between; gap: 16px; margin-bottom: 22px; }
  .bsec-h h1 { font-size: 1.6rem; --fw: 760; font-weight: var(--fw); color: var(--ink-900); }
  .bsec .blog-cats { margin-top: 0; }
  .bsec-h h2 { font-size: 1.35rem; --fw: 740; font-weight: var(--fw); color: var(--ink-900); }
  .bsec-h span { font-size: 0.82rem; color: var(--ink-400); }
  .pfeat { display: grid; grid-template-columns: 1.15fr 1fr; }
  .pfeat .cv { aspect-ratio: auto; min-height: 100%; }
  .pfeat .bd { padding: 34px 34px 32px; gap: 14px; justify-content: center; }
  .pfeat h3 { font-size: clamp(1.25rem, 1rem + 1.1vw, 1.7rem); line-height: 1.65; }
  .pfeat p { font-size: 0.95rem; -webkit-line-clamp: 3; }
  .pfeat .pmeta { margin-top: 6px; }
  /* the lead post: the cover fills the whole block under the header, slightly dimmed, with the text on top */
  .bfeat { background: #061630; }
  .bfeat .pfeat { position: relative; isolation: isolate; display: flex; flex-direction: row; align-items: center; min-height: 80vh; border: 0; border-radius: 0; box-shadow: none; background: none; }
  .bfeat .pfeat:hover { transform: none; box-shadow: none; }
  .bfeat .pfeat .cv { position: absolute; inset: 0; z-index: -2; aspect-ratio: auto; min-height: 0; }
  /* the text sits on the right, so the cover is mirrored to keep its subject clear on the left */
  .bfeat .pfeat .cv img, .bfeat .pfeat:hover .cv img { object-position: 70% 50%; transform: scaleX(-1); }
  .bfeat .pfeat::before {
    content: ""; position: absolute; inset: 0; z-index: -1; pointer-events: none;
    background: linear-gradient(270deg, rgba(6, 22, 48, 0.9) 0%, rgba(6, 22, 48, 0.72) 38%, rgba(6, 22, 48, 0.28) 70%, rgba(6, 22, 48, 0.12) 100%);
  }
  .bfeat .pfeat .bd { flex: 0 1 min(46%, 600px); margin-inline-end: auto; padding: 56px 24px; padding-inline-start: max(34px, calc((100vw - 1200px) / 2 + 34px)); gap: 16px; justify-content: center; }
  .bfeat .kick { font-size: 0.8rem; --fw: 650; font-weight: var(--fw); color: #b9cbe0; }
  .bfeat .pcat { background: #123f8f; color: #fff; }
  .bfeat h2 { font-size: clamp(1.5rem, 1rem + 1.8vw, 2.4rem); --fw: 760; font-weight: var(--fw); line-height: 1.55; color: #fff; }
  .bfeat h2 a { color: #fff; }
  .bfeat h2 a::after { content: ""; position: absolute; inset: 0; }
  .bfeat .pfeat p { font-size: 1.02rem; line-height: 2.1; -webkit-line-clamp: 4; max-width: 46ch; color: #d6e4f5; }
  .bfeat .pmeta { color: #b9cbe0; }
  .bfeat .pmeta i { background: #7f96b3; }
  @media (max-width: 1000px) {
    .bfeat .pfeat { min-height: 72vh; align-items: flex-end; }
    .bfeat .pfeat .cv { aspect-ratio: auto; }
    .bfeat .pfeat .cv img { object-position: 78% 50%; }
    .bfeat .pfeat::before { background: linear-gradient(0deg, rgba(6, 22, 48, 0.94) 0%, rgba(6, 22, 48, 0.78) 45%, rgba(6, 22, 48, 0.2) 100%); }
    .bfeat .pfeat .bd { flex: 1 1 auto; margin: 0; padding: 28px 20px 30px; }
  }
  .tagcloud { display: flex; flex-wrap: wrap; gap: 8px; }
  .tagcloud .bchip::before { content: "#"; color: var(--ink-300); }
  .tagcloud .bchip[aria-current="page"]::before { color: #d8efff; }

  .post-head { padding-block: 40px 0; }
  .post-head .pcat { display: inline-block; margin-bottom: 14px; }
  .post-head h1 { font-size: clamp(1.6rem, 1.1rem + 2.3vw, 2.6rem); --fw: 760; font-weight: var(--fw); line-height: 1.5; color: var(--ink-900); letter-spacing: -0.01em; max-width: 26ch; }
  .post-head .pmeta { margin-top: 16px; font-size: 0.84rem; color: var(--ink-500); }
  .post-cover { margin-top: 28px; border-radius: var(--r-xl); overflow: hidden; border: 1px solid var(--line-soft); box-shadow: var(--sh-2); background: var(--bg-2); }
  .post-cover img { display: block; width: 100%; height: auto; }
  .post-grid { display: grid; grid-template-columns: 300px minmax(0, 1fr); gap: 48px; align-items: start; padding-block: 40px 72px; }
  .pside { order: -1; position: sticky; top: 84px; display: flex; flex-direction: column; gap: 18px; }
  .pside > * { margin: 0; }
  .ptoc, .pcta { border-radius: var(--r-lg); background: var(--surface); border: 1px solid var(--line-soft); box-shadow: var(--sh-1); padding: 20px; }
  .ptoc h2 { font-size: 0.9rem; --fw: 700; font-weight: var(--fw); color: var(--ink-900); margin-bottom: 10px; }
  .ptoc ol { list-style: none; display: flex; flex-direction: column; counter-reset: toc; }
  .ptoc ol, .ptoc li { margin: 0; padding: 0; }
  .ptoc a { display: flex; gap: 9px; padding: 8px 0; border-radius: 0; background: none; font-size: 0.86rem; line-height: 1.8; color: var(--ink-500); border-bottom: 1px dashed var(--line); }
  .ptoc li:last-child a { border-bottom: 0; }
  .ptoc a::before { counter-increment: toc; content: counter(toc, persian); color: var(--ink-300); --fw: 700; font-weight: var(--fw); }
  .ptoc a:hover { color: var(--blue-700); }
  .pcta { background: var(--tint); border-color: var(--blue-100); }
  .pcta b { display: block; font-size: 0.98rem; --fw: 700; font-weight: var(--fw); color: var(--ink-900); line-height: 1.7; }
  .pcta p { font-size: 0.84rem; color: var(--ink-700); line-height: 1.9; margin: 6px 0 14px; }
  .pcta .btn { width: 100%; justify-content: center; }

  .prose { font-size: 1.02rem; line-height: 2.15; color: var(--ink-700); min-width: 0; }
  .prose > p:first-child { font-size: 1.08rem; color: var(--ink-800); }
  .prose h2 { font-size: 1.4rem; --fw: 740; font-weight: var(--fw); color: var(--ink-900); line-height: 1.7; margin: 44px 0 12px; scroll-margin-top: 92px; }
  .prose p { margin-bottom: 16px; }
  .prose ul, .prose ol { margin: 0 0 18px; padding-inline-start: 24px; }
  .prose ul { list-style: disc; } .prose ol { list-style: persian; }
  .prose li { margin-bottom: 8px; padding-inline-start: 4px; }
  .prose li::marker { color: var(--blue-700); --fw: 700; font-weight: var(--fw); }
  .prose a { color: var(--blue-700); border-bottom: 1px solid var(--blue-100); transition: border-color 0.2s; }
  .prose a:hover { border-color: var(--blue); }
  .prose strong { color: var(--ink-900); --fw: 680; font-weight: var(--fw); }
  .prose .note { margin: 22px 0; padding: 16px 18px; border-radius: var(--r-md); background: var(--tint); border: 1px solid var(--blue-100); color: var(--ink-800); font-size: 0.95rem; line-height: 2; }
  .tldr { margin-bottom: 30px; padding: 20px 22px; border-radius: var(--r-lg); background: var(--surface); border: 1px solid var(--line-soft); box-shadow: var(--sh-1); }
  .tldr b { display: block; font-size: 0.92rem; --fw: 700; font-weight: var(--fw); color: var(--ink-900); margin-bottom: 8px; }
  .prose .tldr ul { margin: 0; font-size: 0.95rem; line-height: 2; }
  .tblwrap { overflow-x: auto; margin: 20px 0 24px; border-radius: var(--r-md); border: 1px solid var(--line); background: var(--surface); }
  .prose table { width: 100%; min-width: 460px; border-collapse: collapse; font-size: 0.9rem; line-height: 1.9; }
  .prose th, .prose td { padding: 12px 16px; text-align: start; border-bottom: 1px solid var(--line-soft); }
  .prose th { background: var(--bg-2); color: var(--ink-900); --fw: 680; font-weight: var(--fw); white-space: nowrap; }
  .prose tr:last-child td { border-bottom: 0; }
  .pfaq { margin-top: 12px; display: flex; flex-direction: column; gap: 10px; }
  .pfaq details { border-radius: var(--r-md); background: var(--surface); border: 1px solid var(--line-soft); padding: 0 18px; }
  .pfaq summary { cursor: pointer; list-style: none; padding: 15px 0; font-size: 0.98rem; --fw: 650; font-weight: var(--fw); color: var(--ink-900); display: flex; align-items: center; justify-content: space-between; gap: 12px; }
  .pfaq summary::-webkit-details-marker { display: none; }
  .pfaq summary::after { content: ""; width: 9px; height: 9px; flex: none; border-inline-end: 2px solid var(--ink-400); border-bottom: 2px solid var(--ink-400); transform: rotate(45deg); transition: transform 0.25s; margin-top: -4px; }
  .pfaq details[open] summary::after { transform: rotate(-135deg); margin-top: 4px; }
  .pfaq details p { margin: 0; padding: 0 0 16px; font-size: 0.93rem; color: var(--ink-700); }
  .post-tags { display: flex; flex-wrap: wrap; align-items: center; gap: 8px; margin-top: 34px; padding-top: 22px; border-top: 1px solid var(--line); }
  .post-tags > span { font-size: 0.84rem; color: var(--ink-500); margin-inline-end: 4px; }
  .post-disc { margin-top: 20px; font-size: 0.8rem; color: var(--ink-400); line-height: 1.9; }
  .related { padding-block: 56px; background: var(--surface); border-top: 1px solid var(--line-soft); }
  @media (max-width: 1000px) {
    .pfeat { grid-template-columns: 1fr; } .pfeat .cv { aspect-ratio: 1200 / 630; } .pfeat .bd { padding: 22px 20px 22px; }
    .post-grid { grid-template-columns: 1fr; gap: 22px; padding-block: 26px 52px; }
    .pside { display: contents; }
    .ptoc { order: -1; } .pcta { order: 3; } .post-grid > .prose { order: 0; }
  }
  @media (max-width: 760px) {
    .bsec { padding-block: 36px; } .post-head { padding-top: 26px; } .post-cover { margin-top: 20px; border-radius: var(--r-lg); }
    .prose { font-size: 0.98rem; } .prose h2 { font-size: 1.22rem; margin-top: 34px; }
    .related { padding-block: 40px; }
  }

'''
assert STYLE.count(MARK) == 1
STYLE_BLOG = STYLE.replace(MARK, BLOG_CSS + MARK)

PBG = '<div class="pbg" aria-hidden="true"><span class="aur a1"></span><span class="aur a2"></span><span class="aur a3"></span><span class="gridfloor"></span><span class="fc near" style="left:3%;top:44%;--s:124px;--b:4px;--t:9s;--d:-2s"><img src="assets/coins/btc.webp" alt="" width="200" height="200" decoding="async"></span><span class="fc" style="right:7%;top:14%;--s:84px;--b:0.5px;--t:8s;--d:-5s"><img src="assets/coins/eth.webp" alt="" width="200" height="200" decoding="async"></span><span class="fc far" style="left:21%;top:10%;--s:54px;--b:1.6px;--t:11s;--d:-6s"><img src="assets/coins/usdt.webp" alt="" width="200" height="200" decoding="async"></span><span class="fc near" style="right:-2%;bottom:6%;--s:112px;--b:5px;--t:12s;--d:-7s"><img src="assets/coins/xaut.webp" alt="" width="200" height="200" decoding="async"></span></div>'
CHEV = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m14 6-6 6 6 6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
ARW = '<svg class="arw" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M20 12H4m0 0 6-6m-6 6 6 6" stroke-linecap="round" stroke-linejoin="round"/></svg>'

def crumb(items):
    out = []
    for i, (label, href) in enumerate(items):
        out.append('<a href="%s">%s</a>' % (href, label) if href else '<span>%s</span>' % label)
    return '<nav class="crumb" aria-label="مسیر صفحه">' + CHEV.join(out) + "</nav>"

def crumb_ld(items, self_file):
    els = []
    for i, (label, href) in enumerate(items):
        els.append({"@type": "ListItem", "position": i + 1, "name": label, "item": BASE + (href or self_file).replace("landing.html", "")})
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": els}

def card(p, level="h3", feat=False, lead=False):
    cname = CATS[p["cat"]][0]
    return ('<article class="pcard%s"><a class="cv" href="%s" tabindex="-1" aria-hidden="true"><img src="assets/blog/%s.svg" alt="%s" width="1200" height="630" %s decoding="async"></a>'
            '<div class="bd">%s<a class="pcat" href="blog-cat-%s.html">%s</a><%s><a href="%s">%s</a></%s><p>%s</p>'
            '<div class="pmeta"><time datetime="%s">%s</time><i></i><span>%s دقیقه مطالعه</span></div></div></article>') % (
        " pfeat" if feat else "", p["file"], p["cover"], esc(p["alt"]),
        'fetchpriority="high"' if lead else 'loading="lazy"', '<span class="kick">تازه‌ترین مطلب</span>' if lead else "", p["cat"], cname, level, p["file"], p["title"], level,
        p["excerpt"], p["date"], p["fdate"], fa(p["mins"]))

def cat_chips(current=None):
    out = ['<a class="bchip" href="blog.html"%s>همه‌ی مطالب <span class="n num">%s</span></a>' % (' aria-current="page"' if current == "all" else "", fa(len(POSTS)))]
    for k, (name, _) in CATS.items():
        n = sum(1 for p in POSTS if p["cat"] == k)
        out.append('<a class="bchip" href="blog-cat-%s.html"%s>%s <span class="n num">%s</span></a>' % (k, ' aria-current="page"' if current == k else "", name, fa(n)))
    return '<div class="blog-cats">' + "".join(out) + "</div>"

def tag_cloud(current=None):
    return '<div class="tagcloud">' + "".join(
        '<a class="bchip" href="blog-tag-%s.html"%s>%s</a>' % (k, ' aria-current="page"' if current == k else "", v) for k, v in TAGS.items()) + "</div>"

def page(fname, title, desc, main, lds, og_image="assets/blog/tether.svg", og_type="website", extra_meta=""):
    head = ('<meta charset="utf-8" />\n<title>%s</title>\n<meta name="viewport" content="width=device-width, initial-scale=1" />\n'
            '<meta name="description" content="%s" />\n<link rel="canonical" href="%s" />\n<meta name="robots" content="index, follow, max-image-preview:large" />\n'
            '<meta property="og:type" content="%s" />\n<meta property="og:site_name" content="اکوبیتس" />\n<meta property="og:locale" content="fa_IR" />\n'
            '<meta property="og:title" content="%s" />\n<meta property="og:description" content="%s" />\n<meta property="og:url" content="%s" />\n'
            '<meta property="og:image" content="%s" />\n<meta name="twitter:card" content="summary_large_image" />\n%s') % (
        esc(title), esc(desc), BASE + fname, og_type, esc(title), esc(desc), BASE + fname, BASE + og_image, extra_meta)
    for ld in lds:
        head += '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + "</script>\n"
    out = head + "\n" + STYLE_BLOG + PRE + "<main>\n" + main + "\n" + SIGNUP + POST
    open(fname, "w", encoding="utf8").write(out)

ORG = {"@type": "Organization", "name": "اکوبیتس", "url": BASE}

# ---------------------------------------------------------------- archive
def listing(fname, h1, lead, crumbs, posts, current_cat=None, current_tag=None, title=None, desc=None, featured=False):
    hero = '  <section class="phero">\n    ' + PBG + '\n    <div class="wrap">\n      <div class="rv sec-copy" style="max-width:720px">\n        %s\n        <h1 class="split">%s</h1>\n        <p class="lead">%s</p>\n        %s\n      </div>\n    </div>\n  </section>' % (
        crumb(crumbs), h1, lead, cat_chips(current_cat))
    body, rest = [hero], posts
    if featured and posts:
        body = []      # the archive opens with the lead post; no separate hero
        body.insert(0, '  <section class="bfeat" aria-label="تازه‌ترین مطلب">%s</section>' % card(posts[0], "h2", True, True))
        rest = posts[1:]
    if rest:
        body.append('  <section class="bsec">\n    <div class="wrap">\n      <div class="bsec-h rv"><%s>%s</%s><span class="num">%s مطلب</span></div>%s\n      <div class="pgrid rv stg">%s</div>\n    </div>\n  </section>' % (
            "h1" if featured else "h2", h1 if featured else "مطالب این بخش", "h1" if featured else "h2", fa(len(posts)),
            ('\n      <div class="rv" style="margin:-6px 0 24px">' + cat_chips(current_cat) + "</div>") if featured else "", "".join(card(p) for p in rest)))
    body.append('  <section class="bsec">\n    <div class="wrap">\n      <div class="bsec-h rv"><h2>برچسب‌ها</h2></div>\n      <div class="rv">%s</div>\n    </div>\n  </section>' % tag_cloud(current_tag))
    lds = [crumb_ld(crumbs, fname),
           {"@context": "https://schema.org", "@type": "CollectionPage", "name": h1, "description": desc or lead, "url": BASE + fname,
            "inLanguage": "fa-IR", "isPartOf": {"@type": "Blog", "name": "بلاگ اکوبیتس", "url": BASE + "blog.html"},
            "mainEntity": {"@type": "ItemList", "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "url": BASE + p["file"], "name": p["title"]} for i, p in enumerate(posts)]}}]
    page(fname, title or (h1 + " | بلاگ اکوبیتس"), desc or lead, "\n".join(body), lds, og_image="assets/blog/%s.svg" % (posts[0]["cover"] if posts else "tether"))

listing("blog.html", "بلاگ اکوبیتس",
        "راهنماهای ساده و بدون اصطلاحات پیچیده درباره‌ی خرید و فروش رمزارز با تومان، مفاهیم پایه و دارایی‌های واقعی توکنیزه‌شده.",
        [("خانه", "landing.html"), ("بلاگ", None)], POSTS, current_cat="all", featured=True,
        title="بلاگ اکوبیتس | آموزش و راهنمای خرید رمزارز با تومان",
        desc="آموزش رمزارز به زبان ساده: راهنمای خرید تتر و بیت‌کوین با تومان، مفاهیم پایه و معرفی دارایی‌های واقعی توکنیزه‌شده در بلاگ اکوبیتس.")
for k, (name, d) in CATS.items():
    listing("blog-cat-%s.html" % k, name, d, [("خانه", "landing.html"), ("بلاگ", "blog.html"), (name, None)],
            [p for p in POSTS if p["cat"] == k], current_cat=k, title="%s | بلاگ اکوبیتس" % name, desc=d)
for k, name in TAGS.items():
    ps = [p for p in POSTS if k in p["tags"]]
    listing("blog-tag-%s.html" % k, "برچسب: " + name, "همه‌ی مطالب بلاگ اکوبیتس با برچسب «%s»." % name,
            [("خانه", "landing.html"), ("بلاگ", "blog.html"), (name, None)], ps, current_tag=k,
            title="مطالب با برچسب %s | بلاگ اکوبیتس" % name)

# ---------------------------------------------------------------- posts
for p in POSTS:
    cname = CATS[p["cat"]][0]
    toc, n = [], [0]
    def h2(m):
        n[0] += 1
        toc.append((n[0], m.group(1)))
        return '<h2 id="s%d">%s</h2>' % (n[0], m.group(1))
    body = re.sub(r"<h2>(.*?)</h2>", h2, p["body"].strip())
    faq_html = "".join("<details><summary>%s</summary><p>%s</p></details>" % (q, a) for q, a in p["faq"])
    toc.append((n[0] + 1, "پرسش‌های پرتکرار"))
    crumbs = [("خانه", "landing.html"), ("بلاگ", "blog.html"), (cname, "blog-cat-%s.html" % p["cat"]), (p["title"], None)]
    related = [q for q in POSTS if q is not p][:3]
    main = '''  <article>
  <header class="post-head">
    <div class="wrap">
      %s
      <a class="pcat" href="blog-cat-%s.html">%s</a>
      <h1>%s</h1>
      <div class="pmeta"><span>تحریریه‌ی اکوبیتس</span><i></i><time datetime="%s">%s</time><i></i><span>%s دقیقه مطالعه</span></div>
      <figure class="post-cover"><img src="assets/blog/%s.svg" alt="%s" width="1200" height="630" fetchpriority="high" decoding="async"></figure>
    </div>
  </header>
  <div class="wrap post-grid">
    <div class="prose">
      <div class="tldr"><b>خلاصه‌ی مطلب</b><ul>%s</ul></div>
      %s
      <h2 id="s%d">پرسش‌های پرتکرار</h2>
      <div class="pfaq">%s</div>
      <div class="post-tags"><span>برچسب‌ها:</span>%s</div>
      <p class="post-disc">این مطلب آموزشی است و توصیه‌ی سرمایه‌گذاری نیست. ارزش دارایی‌های دیجیتال نوسان دارد و تصمیم خرید یا فروش با خود شماست.</p>
    </div>
    <aside class="pside">
      <nav class="ptoc" aria-label="فهرست مطالب"><h2>در این مطلب</h2><ol>%s</ol></nav>
      <div class="pcta"><b>%s</b><p>مبلغ تومانی را وارد کنید و قیمت و کارمزد را پیش از تأیید ببینید.</p><a class="btn btn-primary" href="%s">%s %s</a></div>
    </aside>
  </div>
  </article>
  <section class="related">
    <div class="wrap">
      <div class="bsec-h"><h2>مطالب مرتبط</h2><a class="txtlink" href="blog.html" style="font-size:0.86rem;color:var(--blue-700)">همه‌ی مطالب</a></div>
      <div class="pgrid swipe">%s</div>
    </div>
  </section>''' % (
        crumb(crumbs), p["cat"], cname, p["title"], p["date"], p["fdate"], fa(p["mins"]), p["cover"], esc(p["alt"]),
        "".join("<li>%s</li>" % t for t in p["tldr"]), body, n[0] + 1, faq_html,
        "".join('<a class="bchip" href="blog-tag-%s.html">%s</a>' % (t, TAGS[t]) for t in p["tags"]),
        "".join('<li><a href="#s%d">%s</a></li>' % t for t in toc),
        p["cta"][1], p["cta"][0], p["cta"][1], ARW, "".join(card(q) for q in related))
    lds = [crumb_ld(crumbs, p["file"]),
           {"@context": "https://schema.org", "@type": "BlogPosting", "headline": p["title"], "description": p["desc"],
            "image": [BASE + "assets/blog/%s.svg" % p["cover"]], "datePublished": p["date"], "dateModified": p["date"],
            "inLanguage": "fa-IR", "articleSection": cname, "keywords": "، ".join(TAGS[t] for t in p["tags"]),
            "author": ORG, "publisher": ORG, "mainEntityOfPage": {"@type": "WebPage", "@id": BASE + p["file"]}},
           {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
               {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p["faq"]]}]
    page(p["file"], p["seo_title"], p["desc"], main, lds, og_image="assets/blog/%s.svg" % p["cover"], og_type="article",
         extra_meta='<meta property="article:published_time" content="%s" />\n<meta property="article:section" content="%s" />\n' % (p["date"], esc(cname)))

# ---------------------------------------------------------------- home page block
HOME = '''  <!-- BLOG:START (generated by tools/build-blog.py) -->
  <section class="hblog" id="blog">
    <div class="wrap">
      <div class="nhead rv">
        <h2 class="h2">تازه‌ترین مطالب <span class="mute">بلاگ</span></h2>
      </div>
      <div class="pgrid swipe rv stg">%s</div>
      <p class="hblog-more rv"><a class="btn btn-ghost" href="blog.html">همه‌ی مطالب بلاگ %s</a></p>
    </div>
  </section>
  <!-- BLOG:END -->
''' % ("".join(card(p) for p in POSTS[:3]), ARW)
HOME_CSS = CARD_CSS + '''  .hblog { padding-block: 76px; }
  .hblog-more { margin-top: 28px; text-align: center; }
  @media (max-width: 760px) { .hblog { padding-block: 44px; } .hblog-more { margin-top: 10px; } }

'''
idx = open("index.html", encoding="utf8").read()
if "<!-- BLOG:START" in idx:
    a = idx.index("  <!-- BLOG:START"); b = idx.index("<!-- BLOG:END -->") + len("<!-- BLOG:END -->\n")
    idx = idx[:a] + HOME + idx[b:]
elif '  <section class="hfaq" id="home-faq">' in idx:
    anchor = '  <section class="hfaq" id="home-faq">'
    k = idx.index(anchor); k = idx.rfind("\n", 0, idx.rfind("<!--", 0, k)) + 1 if "<!--" in idx[k - 120:k] else k
    idx = idx[:k] + HOME + "\n" + idx[k:]
if "BLOG: post cards" not in idx and "<!-- BLOG:START" in idx:
    assert idx.count(MARK) == 1
    idx = idx.replace(MARK, HOME_CSS + MARK)
open("index.html", "w", encoding="utf8").write(idx)
body = "\n".join(idx.split("\n")[1:]).rstrip()
open("landing.html", "w", encoding="utf8").write(body[:-len("</body></html>")].rstrip("\n") + "\n")

print("built:", ", ".join(["blog.html"] + [p["file"] for p in POSTS]),
      "+ %d category and %d tag pages" % (len(CATS), len(TAGS)))
