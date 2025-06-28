import streamlit as st
import pandas as pd
import joblib
import numpy as np

# --- تهيئة إعدادات الصفحة ---
st.set_page_config(
    page_title="تطبيق توقع الطلب على تأجير السيارات",
    page_icon="🚗",
    layout="centered"
)

# --- تحميل النموذج ---
# هذا النموذج تم تدريبه على بيانات طلب الدراجات، وليس السيارات.
# التنبؤات ستكون غير دقيقة لهذا السبب.
try: # بداية كتلة try
    # تأكد من أن هذا هو مسار واسم ملف موديل توقع الطلب على الدراجات الخاص بك
    # لاحظ المسافة هنا (indentation)
    model = joblib.load('notebooks/models/random_forest_demand_model.joblib')
except FileNotFoundError: # نهاية كتلة try، وبداية كتلة except (نفس مسافة try)
    st.error("ملف النموذج (random_forest_demand_model.joblib) غير موجود! يرجى التأكد من وجوده في مجلد 'models' داخل 'notebooks'.")
    st.stop()

# --- تعريف الأعمدة المتوقعة من بيانات التدريب الأصلية (طلب الدراجات) ---
# هذه الأعمدة هي من موديل تدرب على بيانات طلب الدراجات.
# ستحتاج لتحديث هذه القائمة بالكامل عند تدريب موديل جديد على بيانات طلب السيارات.
expected_columns_bike_demand = [
    'season', 'yr', 'mnth', 'hr', 'holiday', 'weekday', 'workingday',
    'weathersit', 'temp', 'atemp', 'hum', 'windspeed'
]


# --- عنوان التطبيق والوصف ---
st.title('🚗 تطبيق توقع الطلب على تأجير السيارات')
st.write(
    "يساعد هذا التطبيق شركات تأجير السيارات على التنبؤ بالطلب اليومي/الشهري على تأجير السيارات بناءً على العوامل الرئيسية."
)
st.write("---")

# --- مدخلات المستخدم (الجديدة لطلب السيارات) ---
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("معلومات الوقت والموقع")
    prediction_year = st.selectbox('السنة', list(range(2023, 2028)), index=0)
    prediction_month = st.selectbox('الشهر', list(range(1, 13)), index=0)
    prediction_day_of_week = st.selectbox('اليوم من الأسبوع', ['الاحد', 'الاثنين', 'الثلاثاء', 'الاربعاء', 'الخميس', 'الجمعة', 'السبت'])
    prediction_hour = st.slider('الساعة من اليوم (0-23)', 0, 23, 10)

with col2:
    st.subheader("نوع السيارة والعميل")
    car_type = st.selectbox('نوع السيارة المطلوب', ['اقتصادي', 'سيدان', 'دفع رباعي', 'فان', 'فاخرة'])
    rental_location = st.selectbox('موقع التأجير', ['المطار', 'وسط المدينة', 'فندق', 'محلّي', 'آخر'])
    customer_type = st.selectbox('نوع العميل', ['فردي', 'شركات', 'سياح'])

with col3:
    st.subheader("عوامل إضافية")
    # يمكن هنا إضافة عوامل مثل: هل هو حدث خاص؟ طقس؟ (ستحتاج لبيانات لهذه العوامل)
    is_holiday = st.radio('هل هو يوم عطلة أو مناسبة خاصة؟', ['نعم', 'لا'])
    # درجة حرارة وهمية ورطوبة لأن النموذج الحالي يستخدمها
    # هذه المدخلات لن تكون ذات معنى لطلب السيارات بدون موديل جديد
    temp_placeholder = st.slider('درجة الحرارة (تقديرية)', 0.0, 1.0, 0.5, help="تقدير للحرارة، سيتم استخدامه في موديل الدراجات القديم.")
    hum_placeholder = st.slider('الرطوبة (تقديرية)', 0.0, 1.0, 0.5, help="تقدير للرطوبة، سيتم استخدامه في موديل الدراجات القديم.")


# --- منطق التنبؤ ---
if st.button('توقع الطلب', type="primary"):
    # بناء قاموس من المدخلات الجديدة.
    # ملاحظة: هذه المدخلات الجديدة سيتم تحويلها قسرياً لتناسب موديل الدراجات القديم،
    # لذا التنبؤات ستكون غير دقيقة.

    # القيم التي يحتاجها موديل الدراجات (مثال: يرتبط بـ expected_columns_bike_demand)
    # يجب أن تتطابق هذه الأسماء مع أسماء الأعمدة في بيانات تدريب موديل الدراجات
    # ويجب أن يتم تحويل القيم من واجهة المستخدم لتناسبها.
    input_features = {
        'season': prediction_month, # استخدام الشهر كمؤشر للموسم
        'yr': prediction_year - 2011, # تحويل السنة لنسبة كما في بيانات الدراجات
        'mnth': prediction_month,
        'hr': prediction_hour,
        'holiday': 1 if is_holiday == 'نعم' else 0,
        'weekday': ['الاحد', 'الاثنين', 'الثلاثاء', 'الاربعاء', 'الخميس', 'الجمعة', 'السبت'].index(prediction_day_of_week),
        'workingday': 1 if prediction_day_of_week not in ['الجمعة', 'السبت'] and is_holiday == 'لا' else 0,
        'weathersit': 1, # قيمة افتراضية للطقس (clear)
        'temp': temp_placeholder,
        'atemp': temp_placeholder, # قد يكون نفس temp في هذا السياق
        'hum': hum_placeholder,
        'windspeed': 0.2 # قيمة افتراضية
    }

    # تحويل القاموس إلى DataFrame
    input_df_for_prediction = pd.DataFrame([input_features])

    # إعادة ترتيب الأعمدة لتطابق ترتيب أعمدة التدريب لموديل الدراجات بالضبط
    input_df_for_prediction = input_df_for_prediction[expected_columns_bike_demand]

    # إجراء التنبؤ باستخدام النموذج المدرب (موديل الدراجات الحالي)
    predicted_demand = model.predict(input_df_for_prediction)[0]

    st.write("---")
    st.subheader("نتيجة التنبؤ بالطلب:")

    st.success(f" العدد المتوقع للسيارات المطلوبة: {int(predicted_demand)} سيارة")

    st.write("---")
    st.warning("⚠️ ملاحظة هامة جداً: هذا التنبؤ غير دقيق حالياً! الموديل الحالي تم تدريبه على بيانات طلب الدراجات، وليس تأجير السيارات. التنبؤات هي عشوائية وليست ذات صلة.")
    st.info("الخطوة التالية الحاسمة: تدريب موديل ذكاء اصطناعي جديد على بيانات تاريخية حقيقية لطلب تأجير السيارات، ثم تحديث الكود ليعكس هذا الموديل الجديد.")

