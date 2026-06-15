import sys
import os
import jdatetime
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                               QPushButton, QLabel, QGridLayout, QFrame)
from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor, QFont

# تشخیص پلتفرم
is_android = sys.platform.startswith("linux") and "ANDROID" in os.environ

# --- دیتابیس اصلاح شده و با تاریخ دقیق ---
EVENTS_DB = {
    # ==================== فروردین (۱) ====================
    (1, 1): [
        ("جشن بزرگ نوروز و آغاز سال شاهنشاهی", "purple", "جشن باستانی آغاز بهار و شکوفایی طبیعت در ایران‌زمین", "تاریخ بیهقی / اوستا"),
        ("تاج‌گذاری داریوش بزرگ هخامنشی", "orange", "آغاز رسمی پادشاهی داریوش بزرگ و مبدأ گاه‌شماری جدید", "کتیبه بیستون / هرودت")
    ],
    (1, 3): [
        ("زادروز ملکه تاج‌الملوک آیرملو", "orange", "همسر رضا شاه و مادر محمدرضا شاه پهلوی", "کتاب خاطرات ملکه مادر، لندن")
    ],
    (1, 6): [
        ("روز بزرگداشت پیامبر زرتشت", "purple", "یادبود پیامبر آیین یکتاپرستی و حکیم ایرانی", "روایت زرتشتیان / زادروز زرتشت")
    ],
    (1, 13): [
        ("جشن سیزده‌بدر", "purple", "جشن آفرینش آب و پیوند انسان با طبیعت در روز سیزدهم سال", "سنت‌های باستانی ایران")
    ],
    (1, 14): [
        ("زادروز نور پهلوی", "orange", "فرزند شاهزاده رضا پهلوی و یاسمین اعتماد امینی", "بیانیه‌های رسمی دفتر شاهزاده رضا پهلوی")
    ],
    (1, 19): [
        ("جشن فروردینگان", "purple", "روز نیایش و بزرگداشت فروهرها در آیین زرتشتی", "اوستا / بندهش")
    ],
    (1, 24): [
        ("زادروز غلامرضا پهلوی", "orange", "فرزند رضا شاه و ملکه توران امیرسلیمانی", "کتاب خاطرات غلامرضا پهلوی، لندن")
    ],

    # ==================== اردیبهشت (۲) ====================
    (2, 1): [
        ("روز بزرگداشت استاد سعدی شیرازی", "purple", "استاد سخن و از بزرگ‌ترین شاعران و نویسندگان ایران", "تقویم رسمی و اسناد انجمن آثار ملی")
    ],
    (2, 2): [
        ("تاج‌گذاری رضا شاه پهلوی", "orange", "رسمیت یافتن شاهنشاهی رضا شاه پهلوی در کاخ گلستان", "گاهنامه پنجاه سال شاهنشاهی پهلوی، جلد اول"),
        ("جشن ولنجر", "purple", "جشن باستانی آغاز گرما", "آیین‌های بومی ایران باستان")
    ],
    (2, 4): [
        ("بنیان‌گذاری و راه‌اندازی رادیو ایران", "orange", "گشایش نخستین فرستنده رادیویی ایران به فرمان رضا شاه", "آرشیو سازمان صدا و سیما")
    ],
    (2, 7): [
        ("زادروز علیرضا پهلوی (دوم)", "orange", "فرزند دوم محمدرضا شاه پهلوی و ملکه فرح دیبا", "روزنامه اطلاعات، اردیبهشت ۱۳۴۵")
    ],
    (2, 9): [
        ("قانون انحصار قند و شکر", "orange", "تأمین بودجه ساخت راه‌آهن سراسری بدون وام بیگانه توسط رضا شاه", "آرشیو قوانین مجلس شورای ملی")
    ],
    (2, 25): [
        ("روز بزرگداشت حکیم فردوسی", "purple", "خالق شاهنامه و زنده کننده زبان و هویت ایرانی", "وزارت فرهنگ و هنر دوره پهلوی / انجمن مفاخر")
    ],
    (2, 28): [
        ("روز بزرگداشت حکیم عمر خیام نیشابوری", "blue", "ریاضیدان، ستاره‌شناس و شاعر بزرگ ایرانی، خالق تقویم جلالی", "تقویم رسمی کشور / اسناد دانشگاه تهران")
    ],

    # ==================== خرداد (۳) ====================
    (3, 3): [
        ("تصویب قانون فرستادن دانشجو به خارج", "orange", "پرورش نیروی علمی نوین و فرستادن دانشجویان به اروپا توسط رضا شاه", "آرشیو قوانین مجلس، دوره ششم")
    ],
    (3, 6): [
        ("جشن خردادگان", "purple", "جشن باستانی خرداد، روز تکامل آفرینش و بزرگداشت آب‌های پاک", "اوستا"),
        ("روز بزرگداشت شاهنشاهی اشکانیان", "orange", "دودمانی که ۵۰۰ سال ایران را در برابر رومیان پاس داشتند", "تاریخ ایران باستان")
    ],

    # ==================== تیر (۴) ====================
    (4, 1): [
        ("جشن بزرگ تیرگان و یادبود آرش کمانگیر", "purple", "جشن پیروزی ایرانیان بر تورانیان با تیر آرش", "شاهنامه / آثار الباقیه ابوریحان")
    ],
    (4, 4): [
        ("آغاز ساخت راه‌آهن سراسری ایران", "orange", "شروع بزرگ‌ترین پروژه عمرانی کشور به فرمان رضا شاه", "کتاب تاریخ بیست ساله ایران، حسین مکی")
    ],
    (4, 7): [
        ("زادروز مانی", "purple", "پیامبر و هنرمند ایرانی که آیینی عرفانی بنیان نهاد", "تاریخ ادیان باستان")
    ],
    (4, 13): [
        ("زادروز حمیدرضا پهلوی", "orange", "آخرین فرزند رضا شاه پهلوی و ملکه عصمت دولتشاهی", "پرونده‌های سجلی دربار اول")
    ],
    (4, 21): [
        ("واقعه مسجد گوهرشاد مشهد", "orange", "ایستادگی در برابر یکدست‌سازی پوشش و نوسازی‌های رضا شاه", "اسناد مؤسسه مطالعات تاریخ معاصر")
    ],

    # ==================== مرداد (۵) ====================
    (5, 5): [
        ("درگذشت محمدرضا شاه پهلوی", "orange", "درگذشت آخرین پادشاه ایران در قاهره مصر بر اثر بیماری", "بیانیه رسمی دفتر ملکه فرح، قاهره")
    ],
    (5, 14): [
        ("جشن آمردادگان", "purple", "جشن جاودانگی و بی‌مرگی، پیروزی زندگی بر نیستی", "اوستا"),
        ("امضای فرمان مشروطیت", "orange", "آغاز جنبش قانون‌خواهی و محدود شدن قدرت شاه در ایران", "تاریخ معاصر ایران")
    ],
    (5, 28): [
        ("بازگشت شاهنشاهی به ایران (۲۸ مرداد)", "orange", "برکناری دولت مصدق و بازگشت محمدرضاشاه به قدرت", "اسناد معاصر و روزنامه‌های کیهان و اطلاعات")
    ],

    # ==================== شهریور (۶) ====================
    (6, 1): [
        ("آغاز جشن هنر شیراز", "purple", "بزرگ‌ترین فستیوال هنری جهانی ایران با پشتیبانی شهبانو فرح", "اسناد رادیو تلویزیون ملی ایران")
    ],
    (6, 3): [
        ("اشغال ایران در جنگ جهانی دوم", "orange", "ورود نیروهای بیگانه به ایران با وجود اعلام بی‌طرفی در زمان رضا شاه", "اسناد وزارت امور خارجه")
    ],
    (6, 4): [
        ("آغاز ساخت تخت جمشید (پرسپولیس)", "orange", "پایه‌گذاری پایتخت تشریفاتی هخامنشی به فرمان داریوش بزرگ", "لوحه‌های گلی باروی تخت جمشید"),
        ("جشن شهریورگان (روز پدر و مرد ایرانی)", "purple", "روز اراده و اقتدار； بزرگداشت پدران پاسدار خانه و میهن در ایران باستان", "اوستا / آثار الباقیه ابوریحان")
    ],
    (6, 5): [
        ("روز ارتش شاهنشاهی ایران", "orange", "یادبود پدید آمدن ارتش نوین و یکپارچه توسط رضا شاه", "کتاب تاریخ ارتش نوین ایران")
    ],
    (6, 17): [
        ("واقعه میدان ژاله (۱۷ شهریور)", "orange", "رویداد تلخ برخورد ارتش با راهپیمایان آشوب‌طلب در تهران", "روزنامه اطلاعات، شهریور ۱۳۵۷")
    ],
    (6, 21): [
        ("زادروز ایمان پهلوی", "orange", "فرزند دوم شاهزاده رضا پهلوی و یاسمین اعتماد امینی", "وب‌سایت رسمی خاندان پهلوی")
    ],
    (6, 25): [
        ("آغاز پادشاهی محمدرضا شاه پهلوی", "orange", "کناره‌گیری رضا شاه و سوگند خوردن محمدرضا پهلوی در مجلس شورای ملی", "مشروح مذاکرات مجلس، دوره دوازدهم")
    ],

    # ==================== مهر (۷) ====================
    (7, 2): [
        ("جشن بزرگ مهرگان", "purple", "بزرگ‌ترین جشن شاهنشاهی پس از نوروز، روز اعتدال پاییزی و دادگری کوروشی", "شاهنامه / کتب هخامنشی")
    ],
    (7, 7): [
        ("گشودن بابل بدون جنگ توسط کوروش بزرگ", "orange", "ورود ارتش ایران به بابل و پایان امپراتوری بابل نو", "رویدادنامه نبونئید (موزه بریتانیا)")
    ],
    (7, 8): [
        ("نبرد گوگمل", "orange", "شکست داریوش سوم از اسکندر مقدونی و فروپاشی شاهنشاهی هخامنشیان", "چارت‌های فلکی بابلی / کتب یونانی")
    ],
    (7, 9): [
        ("سرکوب گئومات مغ (بردیا دروغین)", "orange", "سرکوب غاصب تخت پادشاهی به دست داریوش بزرگ و یارانش", "کتیبه بیستون داریوش")
    ],
    (7, 20): [
        ("روز بزرگداشت حافظ شیرازی", "purple", "شاعر بزرگ و غزل‌سرای نامی ایران", "تاریخ ادبیات"),
        ("آغاز جشن‌های ۲۵۰۰ ساله شاهنشاهی", "orange", "برگزاری جشن‌های بزرگ تاریخی در تخت جمشید توسط محمدرضا شاه", "کتاب جشن‌های ۲۵۰۰ ساله, وزارت فرهنگ")
    ],
    (7, 22): [
        ("زادروز ملکه فرح دیبا (پهلوی)", "orange", "همسر محمدرضا شاه و اولین شهبانوی تاج‌گذاری‌شده ایران", "کتاب خاطرات فرح پهلوی (کهن‌دیار)")
    ],
    (7, 26): [
        ("تاج‌گذاری محمدرضا شاه پهلوی و شهبانو فرح", "orange", "آیین رسمی تاج‌گذاری پادشاه و شهبانو در کاخ گلستان", "گاهنامه پنجاه سال شاهنشاهی، جلد سوم")
    ],
    (7, 29): [
        ("نگارش منشور حقوق بشر کوروش بزرگ", "orange", "اعلام آزادی دین و برچیدن برده‌داری پس از گشودن بابل", "استوانه گلی کوروش در موزه بریتانیا")
    ],
    (7, 30): [
        ("زادروز schms و اشرف پهلوی", "orange", "خواهر بزرگ‌تر و خواهر دوقلوی محمدرضا شاه پهلوی", "کتاب خاطرات اشرف پهلوی، نیویورک")
    ],

    # ==================== آبان (۸) ====================
    (8, 4): [
        ("زادروز محمدرضا شاه پهلوی", "orange", "دومین پادشاه دودمان پهلوی، زاده شده در تهران", "اسناد دربار شاهنشاهی / کتاب ماموریت برای وطنم")
    ],
    (8, 5): [
        ("زادروز شهناز پهلوی", "orange", "فرزند اول محمدرضا شاه پهلوی و ملکه فوزیه (شاهدخت مصر)", "روزنامه کیهان، آبان ۱۳۱۹")
    ],
    (8, 7): [
        ("روز جهانی کوروش بزرگ", "orange", "روز نمادین گرامی‌داشت کوروش بزرگ به مناسبت ورود به بابل", "قطعنامه بین‌المللی / رویدادنامه نبونئید")
    ],
    (8, 9): [
        ("زادروز شاهزاده رضا پهلوی", "orange", "فرزند ارشد محمدرضا شاه و ملکه فرح", "گاهنامه پنجاه سال شاهنشاهی، جلد سوم"),
        ("پایان دودمان قاجار توسط مجلس", "orange", "برکناری قاجار و واگذاری حکومت موقت به رضا خان پهلوی", "آرشیو قوانین مجلس شورای ملی، دوره پنجم")
    ],
    (8, 10): [
        ("جشن آبانگان", "purple", "جشن باستانی بزرگداشت آب‌های روان و آناهیتا در آیین زرتشتی", "اوستا")
    ],
    (8, 24): [
        ("کندن کانال سوئز باستانی به فرمان داریوش", "orange", "پیوند دادن نیل به دریای سرخ به فرمان داریوش بزرگ", "کتیبه‌های کانال سوئز داریوش در مصر")
    ],

    # ==================== آذر (۹) ====================
    (9, 6): [
        ("برگزاری همایش تهران", "orange", "دیدار روزولت، چرچیل و استالین در تهران در میان جنگ جهانی دوم", "اسناد تاریخی معاصر ایران")
    ],
    (9, 9): [
        ("جشن آذرگان", "purple", "جشن آتش و بزرگداشت آذر, ایزد نگهبان آتش در آیین زرتشتی", "اوستا"),
        ("بازپس‌گیری جزایر سه‌گانه خلیج فارس", "orange", "استقرار ارتش شاهنشاهی در تنب بزرگ، تنب کوچک و ابوموسی", "اسناد وزارت امور خارجه ایران، ۱۳۵۰")
    ],
    (9, 16): [
        ("واقعه روز دانشجو (۱۶ آذر)", "orange", "جان باختن سه دانشجو در دانشگاه تهران در میان آشوب‌های جریان چپ", "آرشیو تاریخی دانشگاه تهران")
    ],
    (9, 20): [
        ("اعلام اصول انقلاب سفید (شاه و ملت)", "orange", "واگذاری زمین‌ها به کشاورزان، اعطای حق رای به زنان و پدید آمدن سپاه دانش", "کتاب انقلاب سفید، محمدرضا پهلوی")
    ],
    (9, 21): [
        ("آزادسازی آذربایجان و ورود ارتش به تبریز", "orange", "پایان غائله فرقه دموکرات پیشه‌وری و پاسداری از مرزهای ایران", "روزنامه اطلاعات، آذر ۱۳۲۵")
    ],
    (9, 24): [
        ("آغاز رسمی دودمان پهلوی", "orange", "ادای سوگند رضا شاه در مجلس شورای ملی و پادشاهی او", "مشروح مذاکرات مجلس، آذر ۱۳۰۴")
    ],
    (9, 30): [
        ("جشن شب یلدا", "purple", "جشن چله بزرگ، بلندترین شب سال و آغاز زمستان", "سنت‌های باستانی ایران")
    ],

    # ==================== دی (۱۰) ====================
    (10, 1): [
        ("جشن دیگان", "purple", "جشن باستانی دی و بزرگداشت دادار اهورامزدا در آیین زرتشتی", "اوستا")
    ],
    (10, 10): [
        ("جشن باستانی بتیکان", "purple", "جشن دهگان و نیایش سرما، تکریم برکت خانه‌ها در ایران کهن", "آثار الباقیه بیرونی")
    ],
    (10, 15): [
        ("بنیان‌گذاری دانشگاه تهران", "orange", "پایه‌گذاری نخستین دانشگاه مدرن ایران به فرمان رضا شاه پهلوی", "آرشیو قوانین مجلس، دوره نهم")
    ],
    (10, 17): [
        ("اجرای قانون کشف حجاب", "orange", "نوسازی پوشش و برچیدن حجاب سنتی به فرمان رضا شاه پهلوی", "گاهنامه پنجاه سال شاهنشاهی پهلوی")
    ],
    (10, 26): [
        ("خروج محمدرضا شاه پهلوی از کشور", "orange", "رهسپار شدن شاه و ملکه فرح از ایران در پی اوج‌گیری شورش ۵۷", "روزنامه اطلاعات، ۲۶ دی ۱۳۵۷"),
        ("زادروز فرح پهلوی دوم", "orange", "فرزند سوم شاهزاده رضا پهلوی و یاسمین اعتماد امینی", "مجله فرانسوی Point de Vue")
    ],

    # ==================== بهمن (۱۱) ====================
    (11, 2): [
        ("جشن بهمنگان", "purple", "جشن بزرگداشت وهومن (اندیشه نیک) و حمایت از جانداران سودمند", "اوستا")
    ],
    (11, 6): [
        ("همه‌پرسی انقلاب سفید", "orange", "تصویب ملی اصلاحات شش‌گانه محمدرضا شاه پهلوی با رای مردم", "وزارت کشور, اسناد همه‌پرسی ۱۳۴۱")
    ],
    (11, 10): [
        ("جشن باستانی سده", "purple", "جشن بزرگ آتش و روشنایی، ۵۰ روز مانده به نوروز", "شاهنامه / التفهیم ابوریحان")
    ],
    (11, 22): [
        ("فروپاشی نظام پادشاهی پهلوی", "orange", "پایان دوران مشروطه سلطنتی در ایران در پی هجوم وحوش ۵۷ بر ضد محمدرضا شاه", "روزنامه‌های کثیرالانتشار، بهمن ۱۳۵۷")
    ],

    # ==================== اسفند (۱۲) ====================
    (12, 5): [
        ("جشن سپندارمذگان (روز عشق، زن و مادر ایرانی)", "purple", "روز عشق پاک، زمین و زایش； بزرگداشت مقام زن و مادر در ایران باستان", "آثار الباقیه بیرونی / اسناد سازمان زنان")
    ],
    (12, 12): [
        ("اعلام نظام تک‌حزبی (حزب رستاخیز)", "orange", "برچیدن احزاب قبلی و معرفی حزب رستاخیز توسط محمدرضا شاه", "روزنامه رستاخیز، اسفند ۱۳۵۳")
    ],
    (12, 22): [
        ("زادروز فرحناز پهلوی", "orange", "فرزند دوم محمدرضا شاه پهلوی و ملکه فرح دیبا", "اسناد بیمارستان حمایت مادران و نوزادان")
    ],
    (12, 24): [
        ("زادروز رضا شاه پهلوی", "orange", "بنیان‌گذار دودمان پهلوی، زاده شده در آلاشت مازندران", "کتاب رضاشاه از تولد تا سلطنت، سید حسن امین")
    ],
    (12, 29): [
        ("ملی شدن صنعت نفت ایران", "orange", "تصویب قانون ملی شدن نفت به رهبری مصدق و پشتیبانی محمدرضا شاه", "مشروح مذاکرات مجلس سنا و شورا")
    ]
}


SHAHANSHAHI_OFFSET = 1180
MONTH_NAMES = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"]

# استایل‌ها (CSS) - دقیقا همان استایل ویندوز
DARK_STYLE = """
QWidget { background-color: #101010; color: #FFFFFF; font-family: 'Segoe UI', sans-serif; }
QPushButton { background-color: #1F2937; color: #FFFFFF; border: none; border-radius: 12px; padding: 8px; font-size: 13px; }
QPushButton#DayButton { background-color: #1F2937; color: #FFFFFF; border-radius: 18px; font-size: 14px; font-weight: bold; }
QPushButton#TodayButton { background-color: #1D4ED8; color: white; border-radius: 18px; font-size: 14px; font-weight: bold; border: none; }
QPushButton#SelectedButton { background-color: #1E3A8A; color: white; border: 2px solid #60A5FA; border-radius: 18px; font-size: 14px; font-weight: bold; }
"""

class CalendarApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("گاهشمار شاهنشاهی")
        
        # سایز صفحه: در اندروید تمام صفحه می‌شود، در ویندوز 400x700
        if is_android:
            self.showFullScreen() 
        else:
            self.resize(400, 700)

        self.is_dark_mode = True
        self.setStyleSheet(DARK_STYLE)
        self.setLayoutDirection(Qt.RightToLeft)

        today_j = jdatetime.date.today()
        self.today_year, self.today_month, self.today_day = today_j.year, today_j.month, today_j.day
        self.view_year, self.view_month, self.selected_day = self.today_year, self.today_month, today_j.day

        self.init_ui()
        self.update_calendar()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(10)

        # هدر
        header_layout = QHBoxLayout()
        self.btn_theme = QPushButton("☀️"); self.btn_theme.setFixedWidth(40); self.btn_theme.clicked.connect(self.toggle_theme)
        self.btn_next_year = QPushButton(">>"); self.btn_next_year.setFixedWidth(40); self.btn_next_year.clicked.connect(lambda: self.change_year(1))
        self.btn_next_month = QPushButton(">"); self.btn_next_month.setFixedWidth(40); self.btn_next_month.clicked.connect(lambda: self.change_month(1))
        self.lbl_header = QLabel(""); self.lbl_header.setAlignment(Qt.AlignCenter); self.lbl_header.setStyleSheet("font-size: 22px; font-weight: bold;")
        self.btn_prev_month = QPushButton("<"); self.btn_prev_month.setFixedWidth(40); self.btn_prev_month.clicked.connect(lambda: self.change_month(-1))
        self.btn_prev_year = QPushButton("<<"); self.btn_prev_year.setFixedWidth(40); self.btn_prev_year.clicked.connect(lambda: self.change_year(-1))

        header_layout.addWidget(self.btn_theme)
        header_layout.addWidget(self.btn_next_year)
        header_layout.addWidget(self.btn_next_month)
        header_layout.addWidget(self.lbl_header, stretch=1)
        header_layout.addWidget(self.btn_prev_month)
        header_layout.addWidget(self.btn_prev_year)
        main_layout.addLayout(header_layout)

        # گرید تقویم
        self.grid_layout = QGridLayout(); self.grid_layout.setSpacing(5)
        days_name = ["ش", "ی", "د", "س", "چ", "پ", "ج"]
        for i, name in enumerate(days_name):
            lbl = QLabel(name); lbl.setAlignment(Qt.AlignCenter); lbl.setStyleSheet("color: #60A5FA; font-weight: bold; font-size: 14px;")
            self.grid_layout.addWidget(lbl, 0, i)

        self.cells = []
        for r in range(6):
            row_cells = []
            for c in range(7):
                btn = QPushButton(""); btn.setObjectName("DayButton"); btn.setFixedHeight(55)
                btn.clicked.connect(lambda _, row=r, col=c: self.select_day(row, col))
                self.grid_layout.addWidget(btn, r + 1, c)
                row_cells.append(btn)
            self.cells.append(row_cells)
        main_layout.addLayout(self.grid_layout)

        # بخش رویدادها
        self.event_frame = QFrame()
        self.event_frame.setStyleSheet("QFrame { background-color: #1F2937; border-radius: 15px; border: 1px solid #374151; }")
        event_layout = QVBoxLayout(self.event_frame)
        self.lbl_event_title = QLabel("رویدادهای روز:"); self.lbl_event_title.setStyleSheet("color: #60A5FA; font-size: 14px; font-weight: bold;")
        self.lbl_events = QLabel(""); self.lbl_events.setWordWrap(True); self.lbl_events.setStyleSheet("color: #D1D5DB; font-size: 14px;")
        event_layout.addWidget(self.lbl_event_title); event_layout.addWidget(self.lbl_events)
        main_layout.addWidget(self.event_frame, stretch=1)

    def toggle_theme(self):
        # پیاده‌سازی ساده تم برای دمو
        pass 

    def select_day(self, row, col):
        btn = self.cells[row][col]
        if hasattr(btn, 'day_val') and btn.day_val is not None:
            self.selected_day = btn.day_val
            self.update_calendar()

    def update_calendar(self):
        raw_year = str(self.view_year + SHAHANSHAHI_OFFSET)
        persian_year = raw_year.translate(str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹"))
        self.lbl_header.setText(f"{MONTH_NAMES[self.view_month-1]} {persian_year} شاهنشاهی")

        start_weekday = (jdatetime.date(self.view_year, self.view_month, 1).weekday() + 7) % 7 
        days_in_month = 31 if self.view_month <= 6 else 30 if self.view_month <= 11 else 29

        for r in range(6):
            for c in range(7):
                btn = self.cells[r][c]; btn.setText(""); btn.setEnabled(False); btn.setObjectName("DayButton"); btn.day_val = None

        day_counter, row, col = 1, 0, start_weekday
        while day_counter <= days_in_month:
            btn = self.cells[row][col]
            is_today = (day_counter == self.today_day and self.view_month == self.today_month and self.view_year == self.today_year)
            is_selected = (day_counter == self.selected_day)
            
            btn.setEnabled(True); btn.day_val = day_counter
            if is_today: btn.setObjectName("TodayButton")
            elif is_selected: btn.setObjectName("SelectedButton")
            else: btn.setObjectName("DayButton")
            btn.style().unpolish(btn); btn.style().polish(btn)

            persian_day = str(day_counter).translate(str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹"))
            btn.setText(persian_day)
            
            # استایل رنگی دکمه‌ها (کپی شده از کد اصلی شما)
            events = EVENTS_DB.get((self.view_month, day_counter), [])
            if events:
                color = events[0][1]
                c_hex = "#C084FC" if color=="purple" else "#FB923C"
                btn.setStyleSheet(f"QPushButton {{ background-color: #1F2937; color: {c_hex}; border-radius: 18px; font-weight: bold; }}")
            else:
                # ریست کردن استایل
                if is_today: btn.setStyleSheet("color: #FFFFFF; background-color: #1D4ED8; border-radius: 18px; font-weight: bold; border: none;")
                elif is_selected: btn.setStyleSheet("color: #FFFFFF; background-color: #1E3A8A; border-radius: 18px; font-weight: bold;")
                else: btn.setStyleSheet("color: #FFFFFF; background-color: #1F2937; border-radius: 18px; font-weight: bold;")

            day_counter += 1; col += 1
            if col > 6: col = 0; row += 1
        
        events = EVENTS_DB.get((self.view_month, self.selected_day), [])
        if events:
            name, color, desc = events[0]
            self.lbl_events.setText(f"{name}\n{desc}")
        else:
            self.lbl_events.setText("رویدادی ثبت نشده")

    def change_month(self, delta):
        self.view_month += delta
        if self.view_month > 12: self.view_month = 1; self.view_year += 1
        elif self.view_month < 1: self.view_month = 12; self.view_year -= 1
        self.update_calendar()

    def change_year(self, delta):
        self.view_year += delta; self.update_calendar()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # تنظیم فونت فارسی برای اندروید (اختیاری)
    # font_id = QFontDatabase.addApplicationFont("fonts/BYekan.ttf")
    # if font_id != -1: app.setFont(QFont("BYekan"))
    
    window = CalendarApp()
    window.show()
    sys.exit(app.exec())