// =============================================================================
// OIL-SIF MULTILINGUAL INTERFACE
// =============================================================================
// The application supports English plus all 22 languages listed in the
// Eighth Schedule of the Constitution of India.
//
// The UI translator below handles the existing hard-coded interface strings
// used throughout the application, so pages do not have to be rewritten one
// by one just to switch language.
// =============================================================================

export const LANGUAGES = [
  'English',
  'हिन्दी (Hindi)',
  'অসমীয়া (Assamese)',
  'বাংলা (Bengali)',
  'ગુજરાતી (Gujarati)',
  'ಕನ್ನಡ (Kannada)',
  'മലയാളം (Malayalam)',
  'मराठी (Marathi)',
  'ଓଡ଼ିଆ (Odia)',
  'ਪੰਜਾਬੀ (Punjabi)',
  'தமிழ் (Tamil)',
  'తెలుగు (Telugu)',
  'اردو (Urdu)',
  'नेपाली (Nepali)',
  'संस्कृत (Sanskrit)',
  'कोंकणी (Konkani)',
  'کٲشُر (Kashmiri)',
  'سنڌي (Sindhi)',
  'बोडो (Bodo)',
  'डोगरी (Dogri)',
  'मैथिली (Maithili)',
  'মৈতৈলোন (Meitei / Manipuri)',
]

const EN = {
  title: 'OIL-SIF COMMAND HUB',
  subtitle: 'Enterprise SIF Precursor Detection & Multilingual Barrier Intelligence Engine',
  welcome: 'Welcome',
  logout: 'Log Out / Back to Login',
  switch_user: 'Switch Role Session',
  select_lang: 'Interface Language',
  field_worker: 'Field Worker',
  hse_officer: 'HSE Officer',
  management: 'Management',
  command_modules: 'Command Modules',
  overview: 'Overview',
  report_analysis: 'Report Analysis',
  intelligence: 'Intelligence',
  ai_copilot: 'AI Copilot',
  my_dashboard: 'My Dashboard',
  facility_node: 'Facility Node',
  engine_telemetry: 'Engine Telemetry',
  sif_classifier: 'SIF Classifier',
  rule_engine: 'Rule Engine',
  multilingual_chatbot: 'Multilingual Chatbot',
  active: 'Active',
  authorized_operator: 'Authorized Operator',
  language: 'Language',
  role_protocol_active: 'Protocol Active',
  terminate_session: 'Terminate Session',
  secure_credential_access: 'Secure Credential Access',
  credential_required: 'Credentials Required',
  role_based_access: 'Role-Based Access',
  authenticated_session: 'Authenticated Session',
  sign_in: 'Sign In',
  register_account: 'Register New Account',
  username: 'Username',
  password: 'Password',
  full_official_name: 'Full Official Name',
  new_username: 'New Username',
  new_password: 'New Password',
  designate_role: 'Designate Role Tier',
  authenticate_access: 'Authenticate Access',
  register_user: 'Register User',
  authenticating: 'Authenticating...',
  creating_account: 'Creating Account...',
  account_created: 'Account created successfully. You can now sign in using your username and password.',
  demo_credentials: 'Demo credentials',
  global_fleet_barrier: 'Global Fleet Barrier Health Telemetry',
  login_required: 'Please sign in to continue.',
  invalid_credentials: 'Invalid username or password.',
  required_field: 'This field is required.',
  all_fields_required: 'All fields are required.',
  loading: 'Loading...',
  loading_intelligence: 'Loading OIL-SIF intelligence...',
  unable_load_dashboard: 'Unable to load dashboard data.',
  no_overview_data: 'No overview data available.',
  failed_load_overview: 'Failed to load overview data',
  total_reports: 'Total Reports',
  all_reports_system: 'All safety reports in the system',
  sif_potential: 'SIF Potential',
  reports_flagged_sif: 'Reports flagged as SIF potential',
  high_sif_probability: 'High SIF Probability',
  reports_high_probability: 'Reports in the high-probability band',
  awaiting_hse_review: 'Awaiting HSE Review',
  reports_pending_validation: 'Reports pending human validation',
  sif_risk_overview: 'SIF Risk Overview',
  distribution_trend: 'Distribution and trend of SIF potential across all reports',
  low_sif_probability: 'Low SIF probability',
  review_zone: 'Review zone',
  high_probability_band: 'High SIF probability',
  top_recurring_precursors: 'Top Recurring Precursors',
  recurring_patterns: 'Recurring activity, hazard and barrier-failure patterns',
  industries_attention: 'Industries Requiring Attention',
  highest_report_volumes: 'Highest report volumes in the public OSHA dataset',
  recent_high_risk: 'Recent High-Risk Reports',
  most_recent_sif: 'Most recent reports classified as SIF potential',
  safety_report_explorer: 'Safety Report Explorer',
  search_select_report: 'Search and select a report from the HSE review dataset',
  search_placeholder: 'Search report ID, activity, precursor or report text...',
  all: 'All',
  pending_review: 'Pending Review',
  selected_safety_report: 'Selected Safety Report',
  full_narrative: 'Full incident / observation narrative',
  no_report_narrative: 'No report narrative available.',
  run_ai_analysis: 'Run AI SIF Analysis',
  analyzing_report: 'Analyzing Report...',
  ai_analysis_result: 'AI Analysis Result',
  model_assisted_screening: 'Model-assisted screening result for HSE validation',
  sif_potential_upper: 'SIF POTENTIAL',
  non_sif_potential: 'NON-SIF POTENTIAL',
  model_backed_analysis: 'Model-backed analysis',
  rule_based_fallback: 'Rule-based fallback',
  analysis_failed: 'Analysis failed.',
  unable_analyze_report: 'Unable to analyze this report.',
  precursor_intelligence: 'Precursor Intelligence',
  recurring_patterns_identified: 'Recurring patterns identified from the safety-report dataset',
  barrier_analysis: 'Barrier Analysis',
  controls_barrier_themes: 'Controls and barrier themes associated with SIF potential',
  life_saving_rules: 'Life-Saving Rules',
  iogp_rule_exposure: 'IOGP rule exposure across the dataset',
  activity_risk: 'Activity Risk',
  activities_ranked: 'Activities ranked using observed SIF potential',
  hse_review_queue: 'HSE Review Queue',
  reports_human_validation: 'Reports requiring human validation before operational use',
  review: 'Review',
  ai_safety_copilot: 'AI Safety Copilot',
  ask_safety_questions: 'Ask questions about SIF risk, precursor patterns, barrier failures, Life-Saving Rules and HSE priorities.',
  ai_copilot_active: 'AI Copilot Active',
  operator: 'Operator',
  user: 'User',
  all_sites: 'All Sites',
  suggested_questions: 'Suggested Questions',
  quick_queries: 'Quick queries for common safety-intelligence tasks',
  dataset_grounded_assistant: 'Dataset-grounded safety intelligence assistant',
  analyzing_safety: 'Analyzing safety intelligence...',
  ask_copilot: 'Ask the OIL-SIF Copilot...',
  send: 'Send →',
  hse_validation_notice: 'HSE Validation Notice',
  ai_validation_note: 'AI responses are intended to support safety intelligence and HSE triage. They should be validated by qualified HSE personnel before operational decisions are made.',
  incident_hazard_scanner: 'Incident & Hazard Precursor Scanner',
  scan_desc: 'AI-assisted real-time screening against IOGP Life-Saving Rules.',
  describe_hazard: 'Describe observed unsafe condition or near miss:',
  scan_btn: 'Scan Hazard with AI Guard',
  critical_detected: 'CRITICAL SIF PRECURSOR DETECTED',
  safe_detected: 'SAFE / LOW-SEVERITY OBSERVATION',
  violated_rule: 'Violated Rule',
  required_action: 'Required Action',
  stop_work: 'Stop Work & Re-establish Physical Barrier',
  field_scenarios: 'Field Safety Scenarios',
  submit_observation: 'Submit an observation to screen it against the IOGP Life-Saving Rules.',
  safe_status: 'SAFE / CONTROLLED',
  hse_dashboard: 'HSE Safety Dashboard',
  management_dashboard: 'Management Dashboard',
  employee_dashboard: 'Employee Dashboard',
}

// Each language pack is intentionally bilingual for safety-critical acronyms
// and standards such as SIF, HSE, IOGP and LOTO.
const PACKS = {
  'हिन्दी (Hindi)': {
    title: 'OIL-SIF कमांड हब', subtitle: 'एंटरप्राइज़ SIF पूर्वसूचक पहचान एवं बहुभाषी बैरियर इंटेलिजेंस इंजन', welcome: 'स्वागत है', logout: 'लॉग आउट / लॉगिन पर वापस जाएँ', switch_user: 'भूमिका सत्र बदलें', select_lang: 'इंटरफ़ेस भाषा', field_worker: 'फील्ड कर्मचारी', hse_officer: 'HSE अधिकारी', management: 'प्रबंधन', command_modules: 'कमांड मॉड्यूल', overview: 'अवलोकन', report_analysis: 'रिपोर्ट विश्लेषण', intelligence: 'इंटेलिजेंस', ai_copilot: 'AI सह-पायलट', my_dashboard: 'मेरा डैशबोर्ड', facility_node: 'सुविधा स्थान', engine_telemetry: 'इंजन टेलीमेट्री', authorized_operator: 'अधिकृत ऑपरेटर', language: 'भाषा', role_protocol_active: 'प्रोटोकॉल सक्रिय', terminate_session: 'सत्र समाप्त करें', secure_credential_access: 'सुरक्षित क्रेडेंशियल एक्सेस', credential_required: 'क्रेडेंशियल आवश्यक', role_based_access: 'भूमिका-आधारित एक्सेस', authenticated_session: 'प्रमाणित सत्र', sign_in: 'साइन इन', register_account: 'नया खाता पंजीकृत करें', username: 'उपयोगकर्ता नाम', password: 'पासवर्ड', full_official_name: 'पूरा आधिकारिक नाम', new_username: 'नया उपयोगकर्ता नाम', new_password: 'नया पासवर्ड', designate_role: 'भूमिका स्तर चुनें', authenticate_access: 'एक्सेस प्रमाणित करें', register_user: 'उपयोगकर्ता पंजीकृत करें', authenticating: 'प्रमाणीकरण हो रहा है...', creating_account: 'खाता बनाया जा रहा है...', account_created: 'खाता सफलतापूर्वक बनाया गया। अब आप उपयोगकर्ता नाम और पासवर्ड से साइन इन कर सकते हैं।', demo_credentials: 'डेमो क्रेडेंशियल', global_fleet_barrier: 'ग्लोबल फ्लीट बैरियर हेल्थ टेलीमेट्री', login_required: 'जारी रखने के लिए कृपया साइन इन करें।', invalid_credentials: 'उपयोगकर्ता नाम या पासवर्ड गलत है।', all_fields_required: 'सभी फ़ील्ड आवश्यक हैं।', loading: 'लोड हो रहा है...', loading_intelligence: 'OIL-SIF इंटेलिजेंस लोड हो रही है...', unable_load_dashboard: 'डैशबोर्ड डेटा लोड नहीं हो सका।', no_overview_data: 'अवलोकन डेटा उपलब्ध नहीं है।', total_reports: 'कुल रिपोर्ट', all_reports_system: 'सिस्टम की सभी सुरक्षा रिपोर्ट', sif_potential: 'SIF संभावित', reports_flagged_sif: 'SIF संभावित के रूप में चिह्नित रिपोर्ट', high_sif_probability: 'उच्च SIF संभावना', reports_high_probability: 'उच्च-संभावना श्रेणी की रिपोर्ट', awaiting_hse_review: 'HSE समीक्षा लंबित', reports_pending_validation: 'मानवीय सत्यापन की प्रतीक्षा में रिपोर्ट', sif_risk_overview: 'SIF जोखिम अवलोकन', distribution_trend: 'सभी रिपोर्टों में SIF संभाव्यता का वितरण और रुझान', low_sif_probability: 'कम SIF संभावना', review_zone: 'समीक्षा क्षेत्र', high_probability_band: 'उच्च SIF संभावना', top_recurring_precursors: 'शीर्ष बार-बार आने वाले पूर्वसूचक', recurring_patterns: 'दोहराए जाने वाले गतिविधि, जोखिम और बैरियर-विफलता पैटर्न', industries_attention: 'ध्यान आवश्यक उद्योग', highest_report_volumes: 'सार्वजनिक OSHA डेटासेट में सर्वाधिक रिपोर्ट मात्रा', recent_high_risk: 'हाल की उच्च-जोखिम रिपोर्ट', most_recent_sif: 'SIF संभावित वर्गीकृत सबसे हाल की रिपोर्ट', safety_report_explorer: 'सुरक्षा रिपोर्ट एक्सप्लोरर', search_select_report: 'HSE समीक्षा डेटासेट से रिपोर्ट खोजें और चुनें', search_placeholder: 'रिपोर्ट ID, गतिविधि, पूर्वसूचक या रिपोर्ट टेक्स्ट खोजें...', all: 'सभी', pending_review: 'समीक्षा लंबित', selected_safety_report: 'चयनित सुरक्षा रिपोर्ट', full_narrative: 'पूर्ण घटना / अवलोकन विवरण', no_report_narrative: 'रिपोर्ट विवरण उपलब्ध नहीं है।', run_ai_analysis: 'AI SIF विश्लेषण चलाएँ', analyzing_report: 'रिपोर्ट का विश्लेषण हो रहा है...', ai_analysis_result: 'AI विश्लेषण परिणाम', model_assisted_screening: 'HSE सत्यापन के लिए मॉडल-सहायित स्क्रीनिंग परिणाम', sif_potential_upper: 'SIF संभावित', non_sif_potential: 'SIF संभावित नहीं', model_backed_analysis: 'मॉडल-आधारित विश्लेषण', rule_based_fallback: 'नियम-आधारित वैकल्पिक विश्लेषण', analysis_failed: 'विश्लेषण विफल हुआ।', unable_analyze_report: 'इस रिपोर्ट का विश्लेषण नहीं हो सका।', precursor_intelligence: 'पूर्वसूचक इंटेलिजेंस', recurring_patterns_identified: 'सुरक्षा-रिपोर्ट डेटासेट से पहचाने गए बार-बार आने वाले पैटर्न', barrier_analysis: 'बैरियर विश्लेषण', controls_barrier_themes: 'SIF संभाव्यता से जुड़े नियंत्रण और बैरियर थीम', life_saving_rules: 'Life-Saving Rules', iogp_rule_exposure: 'डेटासेट में IOGP नियम एक्सपोज़र', activity_risk: 'गतिविधि जोखिम', activities_ranked: 'देखी गई SIF संभाव्यता के आधार पर क्रमबद्ध गतिविधियाँ', hse_review_queue: 'HSE समीक्षा कतार', reports_human_validation: 'ऑपरेशनल उपयोग से पहले मानवीय सत्यापन आवश्यक रिपोर्ट', review: 'समीक्षा', ai_safety_copilot: 'AI सुरक्षा सह-पायलट', ask_safety_questions: 'SIF जोखिम, पूर्वसूचक पैटर्न, बैरियर विफलताओं, Life-Saving Rules और HSE प्राथमिकताओं के बारे में प्रश्न पूछें।', ai_copilot_active: 'AI Copilot सक्रिय', operator: 'ऑपरेटर', user: 'उपयोगकर्ता', all_sites: 'सभी साइटें', suggested_questions: 'सुझाए गए प्रश्न', quick_queries: 'सामान्य सुरक्षा-इंटेलिजेंस कार्यों के लिए त्वरित प्रश्न', dataset_grounded_assistant: 'डेटासेट-आधारित सुरक्षा इंटेलिजेंस सहायक', analyzing_safety: 'सुरक्षा इंटेलिजेंस का विश्लेषण हो रहा है...', ask_copilot: 'OIL-SIF Copilot से पूछें...', send: 'भेजें →', hse_validation_notice: 'HSE सत्यापन सूचना', ai_validation_note: 'AI प्रतिक्रियाएँ सुरक्षा इंटेलिजेंस और HSE ट्रायेज में सहायता के लिए हैं। ऑपरेशनल निर्णयों से पहले योग्य HSE कर्मियों द्वारा उनका सत्यापन किया जाना चाहिए।', incident_hazard_scanner: 'घटना एवं खतरा पूर्वसूचक स्कैनर', scan_desc: 'IOGP Life-Saving Rules के विरुद्ध AI-सहायित रीयल-टाइम स्क्रीनिंग।', describe_hazard: 'देखी गई असुरक्षित स्थिति या निकट-चूक का विवरण दें:', scan_btn: 'AI Guard से खतरा स्कैन करें', critical_detected: 'गंभीर SIF पूर्वसूचक पाया गया', safe_detected: 'सुरक्षित / कम-गंभीरता अवलोकन', violated_rule: 'उल्लंघन किया गया नियम', required_action: 'आवश्यक कार्रवाई', stop_work: 'काम रोकें और भौतिक बैरियर पुनः स्थापित करें', field_scenarios: 'फील्ड सुरक्षा परिदृश्य', submit_observation: 'IOGP Life-Saving Rules के विरुद्ध जाँच के लिए अवलोकन जमा करें।', safe_status: 'सुरक्षित / नियंत्रित', hse_dashboard: 'HSE सुरक्षा डैशबोर्ड', management_dashboard: 'प्रबंधन डैशबोर्ड', employee_dashboard: 'कर्मचारी डैशबोर्ड'
  },
  'অসমীয়া (Assamese)': {
    title: 'OIL-SIF কমাণ্ড হাব', subtitle: 'এণ্টাৰপ্ৰাইজ SIF পূৰ্বসূচক চিনাক্তকৰণ আৰু বহুভাষিক বেৰিয়াৰ ইণ্টেলিজেন্স ইঞ্জিন', welcome: 'স্বাগতম', logout: 'লগ আউট / লগইনলৈ উভতি যাওক', select_lang: 'ইণ্টাৰফেচ ভাষা', field_worker: 'ফিল্ড কৰ্মী', hse_officer: 'HSE বিষয়া', management: 'পৰিচালনা', command_modules: 'কমাণ্ড মডিউল', overview: 'অভাৰভিউ', report_analysis: 'ৰিপৰ্ট বিশ্লেষণ', intelligence: 'ইণ্টেলিজেন্স', ai_copilot: 'AI কো-পাইলট', my_dashboard: 'মোৰ ডেশ্বব’ৰ্ড', facility_node: 'ফেচিলিটি নোড', engine_telemetry: 'ইঞ্জিন টেলিমেট্ৰী', authorized_operator: 'অনুমোদিত অপাৰেটৰ', language: 'ভাষা', role_protocol_active: 'প্ৰটোকল সক্ৰিয়', terminate_session: 'ছেছন সমাপ্ত কৰক', secure_credential_access: 'সুৰক্ষিত ক্ৰেডেনশিয়েল প্ৰৱেশ', credential_required: 'ক্ৰেডেনশিয়েল আৱশ্যক', role_based_access: 'ভূমিকাভিত্তিক প্ৰৱেশ', authenticated_session: 'প্ৰমাণিত ছেছন', sign_in: 'ছাইন ইন', register_account: 'নতুন একাউণ্ট পঞ্জীয়ন', username: 'ব্যৱহাৰকাৰীৰ নাম', password: 'পাছৱৰ্ড', full_official_name: 'সম্পূৰ্ণ চৰকাৰী নাম', new_username: 'নতুন ব্যৱহাৰকাৰীৰ নাম', new_password: 'নতুন পাছৱৰ্ড', designate_role: 'ভূমিকা স্তৰ নিৰ্ধাৰণ কৰক', authenticate_access: 'প্ৰৱেশ প্ৰমাণিত কৰক', register_user: 'ব্যৱহাৰকাৰী পঞ্জীয়ন কৰক', authenticating: 'প্ৰমাণীকৰণ চলি আছে...', creating_account: 'একাউণ্ট সৃষ্টি কৰা হৈছে...', account_created: 'একাউণ্ট সফলভাৱে সৃষ্টি হৈছে। এতিয়া ব্যৱহাৰকাৰীৰ নাম আৰু পাছৱৰ্ডেৰে ছাইন ইন কৰিব পাৰে।', demo_credentials: 'ডেমো ক্ৰেডেনশিয়েল', global_fleet_barrier: 'গ্লোবেল ফ্লীট বেৰিয়াৰ হেল্থ টেলিমেট্ৰী', login_required: 'আগবাঢ়িবলৈ অনুগ্ৰহ কৰি ছাইন ইন কৰক।', invalid_credentials: 'ব্যৱহাৰকাৰীৰ নাম বা পাছৱৰ্ড ভুল।', all_fields_required: 'সকলো ফিল্ড আৱশ্যক।', loading: 'লোড হৈ আছে...', loading_intelligence: 'OIL-SIF ইণ্টেলিজেন্স লোড হৈ আছে...', unable_load_dashboard: 'ডেশ্বব’ৰ্ড ডাটা লোড কৰিব পৰা নগ’ল।', no_overview_data: 'অভাৰভিউ ডাটা উপলব্ধ নহয়।', total_reports: 'মুঠ ৰিপৰ্ট', all_reports_system: 'চিষ্টেমৰ সকলো সুৰক্ষা ৰিপৰ্ট', sif_potential: 'SIF সম্ভাৱনা', reports_flagged_sif: 'SIF সম্ভাৱনা হিচাপে চিহ্নিত ৰিপৰ্ট', high_sif_probability: 'উচ্চ SIF সম্ভাৱনা', reports_high_probability: 'উচ্চ-সম্ভাৱনা শ্ৰেণীৰ ৰিপৰ্ট', awaiting_hse_review: 'HSE পৰ্যালোচনা অপেক্ষাৰত', reports_pending_validation: 'মানৱ যাচাইৰ বাবে অপেক্ষাৰত ৰিপৰ্ট', sif_risk_overview: 'SIF বিপদৰ অভাৰভিউ', distribution_trend: 'সকলো ৰিপৰ্টত SIF সম্ভাৱনাৰ বিতৰণ আৰু ধাৰা', low_sif_probability: 'কম SIF সম্ভাৱনা', review_zone: 'পৰ্যালোচনা অঞ্চল', high_probability_band: 'উচ্চ SIF সম্ভাৱনা', top_recurring_precursors: 'শীৰ্ষ পুনৰাবৃত্ত পূৰ্বসূচক', recurring_patterns: 'পুনৰাবৃত্ত কাৰ্য, বিপদ আৰু বেৰিয়াৰ-বিফলতাৰ ধাৰা', industries_attention: 'মনোযোগৰ প্ৰয়োজন হোৱা উদ্যোগ', recent_high_risk: 'শেহতীয়া উচ্চ-বিপদ ৰিপৰ্ট', most_recent_sif: 'শেহতীয়া SIF সম্ভাৱ্য ৰিপৰ্ট', safety_report_explorer: 'সুৰক্ষা ৰিপৰ্ট এক্সপ্ল’ৰাৰ', search_select_report: 'HSE পৰ্যালোচনা ডেটাছেটৰ পৰা ৰিপৰ্ট বিচাৰি বাছনি কৰক', search_placeholder: 'ৰিপৰ্ট ID, কাৰ্য, পূৰ্বসূচক বা ৰিপৰ্ট টেক্সট বিচাৰক...', all: 'সকলো', pending_review: 'পৰ্যালোচনা অপেক্ষাৰত', selected_safety_report: 'নিৰ্বাচিত সুৰক্ষা ৰিপৰ্ট', full_narrative: 'সম্পূৰ্ণ ঘটনা / পৰ্যবেক্ষণ বিৱৰণ', no_report_narrative: 'ৰিপৰ্টৰ বিৱৰণ উপলব্ধ নহয়।', run_ai_analysis: 'AI SIF বিশ্লেষণ চলাওক', analyzing_report: 'ৰিপৰ্ট বিশ্লেষণ হৈ আছে...', ai_analysis_result: 'AI বিশ্লেষণৰ ফলাফল', precursor_intelligence: 'পূৰ্বসূচক ইণ্টেলিজেন্স', barrier_analysis: 'বেৰিয়াৰ বিশ্লেষণ', life_saving_rules: 'Life-Saving Rules', activity_risk: 'কাৰ্যৰ বিপদ', hse_review_queue: 'HSE পৰ্যালোচনা শাৰী', review: 'পৰ্যালোচনা', ai_safety_copilot: 'AI সুৰক্ষা কো-পাইলট', suggested_questions: 'প্ৰস্তাৱিত প্ৰশ্ন', quick_queries: 'সাধাৰণ সুৰক্ষা-ইণ্টেলিজেন্স কামৰ বাবে দ্ৰুত প্ৰশ্ন', dataset_grounded_assistant: 'ডেটাছেট-ভিত্তিক সুৰক্ষা ইণ্টেলিজেন্স সহায়ক', analyzing_safety: 'সুৰক্ষা ইণ্টেলিজেন্স বিশ্লেষণ হৈ আছে...', ask_copilot: 'OIL-SIF Copilotক সোধক...', send: 'পঠিয়াওক →', hse_validation_notice: 'HSE যাচাই জাননী', incident_hazard_scanner: 'ঘটনা আৰু বিপদ পূৰ্বসূচক স্কেনাৰ', describe_hazard: 'দেখা অসুৰক্ষিত অৱস্থা বা নিকট-দুৰ্ঘটনাৰ বিৱৰণ দিয়ক:', scan_btn: 'AI Guardৰে বিপদ স্কেন কৰক', critical_detected: 'গুৰুতৰ SIF পূৰ্বসূচক ধৰা পৰিছে', safe_detected: 'নিৰাপদ / কম-গুৰুতৰ পৰ্যবেক্ষণ', violated_rule: 'উলংঘন কৰা নিয়ম', required_action: 'প্ৰয়োজনীয় পদক্ষেপ', stop_work: 'কাম বন্ধ কৰক আৰু ভৌতিক বেৰিয়াৰ পুনঃস্থাপন কৰক', field_scenarios: 'ফিল্ড সুৰক্ষা পৰিস্থিতি', safe_status: 'নিৰাপদ / নিয়ন্ত্ৰিত', hse_dashboard: 'HSE সুৰক্ষা ডেশ্বব’ৰ্ড', management_dashboard: 'পৰিচালনা ডেশ্বব’ৰ্ড', employee_dashboard: 'কৰ্মচাৰী ডেশ্বব’ৰ্ড'
  },
  'বাংলা (Bengali)': {
    title: 'OIL-SIF কমান্ড হাব', subtitle: 'এন্টারপ্রাইজ SIF পূর্বসূচক শনাক্তকরণ ও বহুভাষিক ব্যারিয়ার ইন্টেলিজেন্স ইঞ্জিন', welcome: 'স্বাগতম', logout: 'লগ আউট / লগইনে ফিরুন', select_lang: 'ইন্টারফেস ভাষা', field_worker: 'ফিল্ড কর্মী', hse_officer: 'HSE কর্মকর্তা', management: 'ব্যবস্থাপনা', command_modules: 'কমান্ড মডিউল', overview: 'ওভারভিউ', report_analysis: 'রিপোর্ট বিশ্লেষণ', intelligence: 'ইন্টেলিজেন্স', ai_copilot: 'AI কো-পাইলট', my_dashboard: 'আমার ড্যাশবোর্ড', facility_node: 'ফ্যাসিলিটি নোড', engine_telemetry: 'ইঞ্জিন টেলিমেট্রি', authorized_operator: 'অনুমোদিত অপারেটর', language: 'ভাষা', role_protocol_active: 'প্রোটোকল সক্রিয়', terminate_session: 'সেশন শেষ করুন', secure_credential_access: 'নিরাপদ ক্রেডেনশিয়াল অ্যাক্সেস', credential_required: 'ক্রেডেনশিয়াল প্রয়োজন', role_based_access: 'ভূমিকা-ভিত্তিক অ্যাক্সেস', authenticated_session: 'প্রমাণীকৃত সেশন', sign_in: 'সাইন ইন', register_account: 'নতুন অ্যাকাউন্ট নিবন্ধন', username: 'ইউজারনেম', password: 'পাসওয়ার্ড', full_official_name: 'পূর্ণ সরকারি নাম', new_username: 'নতুন ইউজারনেম', new_password: 'নতুন পাসওয়ার্ড', designate_role: 'ভূমিকা স্তর নির্ধারণ করুন', authenticate_access: 'অ্যাক্সেস প্রমাণীকরণ করুন', register_user: 'ব্যবহারকারী নিবন্ধন করুন', authenticating: 'প্রমাণীকরণ চলছে...', creating_account: 'অ্যাকাউন্ট তৈরি হচ্ছে...', account_created: 'অ্যাকাউন্ট সফলভাবে তৈরি হয়েছে। এখন ইউজারনেম ও পাসওয়ার্ড দিয়ে সাইন ইন করুন।', demo_credentials: 'ডেমো ক্রেডেনশিয়াল', global_fleet_barrier: 'গ্লোবাল ফ্লিট ব্যারিয়ার হেলথ টেলিমেট্রি', login_required: 'চালিয়ে যেতে সাইন ইন করুন।', invalid_credentials: 'ইউজারনেম বা পাসওয়ার্ড ভুল।', all_fields_required: 'সব ফিল্ড আবশ্যক।', loading: 'লোড হচ্ছে...', loading_intelligence: 'OIL-SIF ইন্টেলিজেন্স লোড হচ্ছে...', unable_load_dashboard: 'ড্যাশবোর্ড ডেটা লোড করা যায়নি।', no_overview_data: 'কোনও ওভারভিউ ডেটা নেই।', total_reports: 'মোট রিপোর্ট', all_reports_system: 'সিস্টেমের সব নিরাপত্তা রিপোর্ট', sif_potential: 'SIF সম্ভাবনা', reports_flagged_sif: 'SIF সম্ভাবনা হিসেবে চিহ্নিত রিপোর্ট', high_sif_probability: 'উচ্চ SIF সম্ভাবনা', reports_high_probability: 'উচ্চ-সম্ভাবনা ব্যান্ডের রিপোর্ট', awaiting_hse_review: 'HSE পর্যালোচনা অপেক্ষমাণ', reports_pending_validation: 'মানব যাচাইয়ের জন্য অপেক্ষমাণ রিপোর্ট', sif_risk_overview: 'SIF ঝুঁকি ওভারভিউ', distribution_trend: 'সব রিপোর্টে SIF সম্ভাবনার বণ্টন ও প্রবণতা', low_sif_probability: 'কম SIF সম্ভাবনা', review_zone: 'পর্যালোচনা অঞ্চল', high_probability_band: 'উচ্চ SIF সম্ভাবনা', top_recurring_precursors: 'শীর্ষ পুনরাবৃত্ত পূর্বসূচক', recurring_patterns: 'পুনরাবৃত্ত কার্যকলাপ, ঝুঁকি ও ব্যারিয়ার-ব্যর্থতার প্যাটার্ন', recent_high_risk: 'সাম্প্রতিক উচ্চ-ঝুঁকির রিপোর্ট', safety_report_explorer: 'সেফটি রিপোর্ট এক্সপ্লোরার', search_select_report: 'HSE পর্যালোচনা ডেটাসেট থেকে রিপোর্ট খুঁজে বেছে নিন', search_placeholder: 'রিপোর্ট ID, কার্যকলাপ, পূর্বসূচক বা রিপোর্ট টেক্সট খুঁজুন...', all: 'সব', pending_review: 'পর্যালোচনা অপেক্ষমাণ', selected_safety_report: 'নির্বাচিত সেফটি রিপোর্ট', full_narrative: 'সম্পূর্ণ ঘটনা / পর্যবেক্ষণ বিবরণ', no_report_narrative: 'রিপোর্টের বিবরণ নেই।', run_ai_analysis: 'AI SIF বিশ্লেষণ চালান', analyzing_report: 'রিপোর্ট বিশ্লেষণ চলছে...', ai_analysis_result: 'AI বিশ্লেষণ ফলাফল', precursor_intelligence: 'পূর্বসূচক ইন্টেলিজেন্স', barrier_analysis: 'ব্যারিয়ার বিশ্লেষণ', life_saving_rules: 'Life-Saving Rules', activity_risk: 'কার্যকলাপ ঝুঁকি', hse_review_queue: 'HSE পর্যালোচনা সারি', review: 'পর্যালোচনা', ai_safety_copilot: 'AI সেফটি কো-পাইলট', suggested_questions: 'প্রস্তাবিত প্রশ্ন', quick_queries: 'সাধারণ সেফটি-ইন্টেলিজেন্স কাজের দ্রুত প্রশ্ন', dataset_grounded_assistant: 'ডেটাসেট-ভিত্তিক নিরাপত্তা ইন্টেলিজেন্স সহায়ক', analyzing_safety: 'সেফটি ইন্টেলিজেন্স বিশ্লেষণ হচ্ছে...', ask_copilot: 'OIL-SIF Copilot-কে জিজ্ঞাসা করুন...', send: 'পাঠান →', hse_validation_notice: 'HSE যাচাই নোটিশ', incident_hazard_scanner: 'ঘটনা ও ঝুঁকি পূর্বসূচক স্ক্যানার', describe_hazard: 'দেখা অনিরাপদ অবস্থা বা নিকট-দুর্ঘটনার বর্ণনা দিন:', scan_btn: 'AI Guard দিয়ে ঝুঁকি স্ক্যান করুন', critical_detected: 'গুরুতর SIF পূর্বসূচক শনাক্ত হয়েছে', safe_detected: 'নিরাপদ / কম-গুরুতর পর্যবেক্ষণ', violated_rule: 'লঙ্ঘিত নিয়ম', required_action: 'প্রয়োজনীয় পদক্ষেপ', stop_work: 'কাজ বন্ধ করুন এবং শারীরিক ব্যারিয়ার পুনঃস্থাপন করুন', field_scenarios: 'ফিল্ড সেফটি পরিস্থিতি', safe_status: 'নিরাপদ / নিয়ন্ত্রিত', hse_dashboard: 'HSE সেফটি ড্যাশবোর্ড', management_dashboard: 'ম্যানেজমেন্ট ড্যাশবোর্ড', employee_dashboard: 'কর্মচারী ড্যাশবোর্ড'
  },
  'ગુજરાતી (Gujarati)': {
    title: 'OIL-SIF કમાન્ડ હબ', subtitle: 'એન્ટરપ્રાઇઝ SIF પૂર્વસૂચક ઓળખ અને બહુભાષી બેરિયર ઇન્ટેલિજન્સ એન્જિન', welcome: 'સ્વાગત છે', logout: 'લોગ આઉટ / લોગિન પર પાછા જાઓ', select_lang: 'ઇન્ટરફેસ ભાષા', field_worker: 'ફીલ્ડ કર્મચારી', hse_officer: 'HSE અધિકારી', management: 'વ્યવસ્થાપન', command_modules: 'કમાન્ડ મોડ્યુલ્સ', overview: 'ઝાંખી', report_analysis: 'રિપોર્ટ વિશ્લેષણ', intelligence: 'ઇન્ટેલિજન્સ', ai_copilot: 'AI કોપાઇલોટ', my_dashboard: 'મારું ડેશબોર્ડ', facility_node: 'ફેસિલિટી નોડ', engine_telemetry: 'એન્જિન ટેલિમેટ્રી', authorized_operator: 'અધિકૃત ઓપરેટર', language: 'ભાષા', role_protocol_active: 'પ્રોટોકોલ સક્રિય', terminate_session: 'સત્ર સમાપ્ત કરો', secure_credential_access: 'સુરક્ષિત ક્રેડેન્શિયલ ઍક્સેસ', credential_required: 'ક્રેડેન્શિયલ જરૂરી', role_based_access: 'ભૂમિકા આધારિત ઍક્સેસ', authenticated_session: 'પ્રમાણિત સત્ર', sign_in: 'સાઇન ઇન', register_account: 'નવું એકાઉન્ટ નોંધણી', username: 'વપરાશકર્તા નામ', password: 'પાસવર્ડ', full_official_name: 'પૂર્ણ સત્તાવાર નામ', new_username: 'નવું વપરાશકર્તા નામ', new_password: 'નવો પાસવર્ડ', designate_role: 'ભૂમિકા સ્તર પસંદ કરો', authenticate_access: 'ઍક્સેસ પ્રમાણિત કરો', register_user: 'વપરાશકર્તા નોંધણી કરો', authenticating: 'પ્રમાણીકરણ થઈ રહ્યું છે...', creating_account: 'એકાઉન્ટ બનાવાઈ રહ્યું છે...', account_created: 'એકાઉન્ટ સફળતાપૂર્વક બનાવાયું. હવે વપરાશકર્તા નામ અને પાસવર્ડથી સાઇન ઇન કરી શકો છો.', demo_credentials: 'ડેમો ક્રેડેન્શિયલ્સ', global_fleet_barrier: 'ગ્લોબલ ફલિટ બેરિયર હેલ્થ ટેલિમેટ્રી', login_required: 'ચાલુ રાખવા માટે સાઇન ઇન કરો.', invalid_credentials: 'વપરાશકર્તા નામ અથવા પાસવર્ડ ખોટો છે.', all_fields_required: 'બધી ફીલ્ડ જરૂરી છે.', loading: 'લોડ થઈ રહ્યું છે...', loading_intelligence: 'OIL-SIF ઇન્ટેલિજન્સ લોડ થઈ રહી છે...', unable_load_dashboard: 'ડેશબોર્ડ ડેટા લોડ થઈ શક્યો નથી.', total_reports: 'કુલ રિપોર્ટ્સ', sif_potential: 'SIF સંભાવના', high_sif_probability: 'ઉચ્ચ SIF સંભાવના', awaiting_hse_review: 'HSE સમીક્ષા બાકી', reports_pending_validation: 'માનવીય ચકાસણી બાકી રિપોર્ટ્સ', sif_risk_overview: 'SIF જોખમ ઝાંખી', low_sif_probability: 'ઓછી SIF સંભાવના', review_zone: 'સમીક્ષા ક્ષેત્ર', high_probability_band: 'ઉચ્ચ SIF સંભાવના', top_recurring_precursors: 'મુખ્ય પુનરાવર્તિત પૂર્વસૂચકો', recent_high_risk: 'તાજેતરના ઉચ્ચ જોખમ રિપોર્ટ્સ', safety_report_explorer: 'સેફ્ટી રિપોર્ટ એક્સપ્લોરર', search_placeholder: 'રિપોર્ટ ID, પ્રવૃત્તિ, પૂર્વસૂચક અથવા રિપોર્ટ ટેક્સ્ટ શોધો...', all: 'બધા', pending_review: 'સમીક્ષા બાકી', selected_safety_report: 'પસંદ કરાયેલ સેફ્ટી રિપોર્ટ', run_ai_analysis: 'AI SIF વિશ્લેષણ ચલાવો', analyzing_report: 'રિપોર્ટનું વિશ્લેષણ થઈ રહ્યું છે...', ai_analysis_result: 'AI વિશ્લેષણ પરિણામ', precursor_intelligence: 'પૂર્વસૂચક ઇન્ટેલિજન્સ', barrier_analysis: 'બેરિયર વિશ્લેષણ', life_saving_rules: 'Life-Saving Rules', activity_risk: 'પ્રવૃત્તિ જોખમ', hse_review_queue: 'HSE સમીક્ષા કતાર', review: 'સમીક્ષા', ai_safety_copilot: 'AI સેફ્ટી કોપાઇલોટ', suggested_questions: 'સૂચવેલા પ્રશ્નો', quick_queries: 'સામાન્ય સેફ્ટી-ઇન્ટેલિજન્સ કાર્યો માટે ઝડપી પ્રશ્નો', dataset_grounded_assistant: 'ડેટાસેટ આધારિત સેફ્ટી ઇન્ટેલિજન્સ સહાયક', analyzing_safety: 'સેફ્ટી ઇન્ટેલિજન્સનું વિશ્લેષણ થઈ રહ્યું છે...', ask_copilot: 'OIL-SIF Copilotને પૂછો...', send: 'મોકલો →', hse_validation_notice: 'HSE ચકાસણી સૂચના', incident_hazard_scanner: 'ઘટના અને જોખમ પૂર્વસૂચક સ્કેનર', describe_hazard: 'જોવામાં આવેલી અસુરક્ષિત સ્થિતિ અથવા નજીકની ઘટનાનું વર્ણન આપો:', scan_btn: 'AI Guardથી જોખમ સ્કેન કરો', critical_detected: 'ગંભીર SIF પૂર્વસૂચક મળ્યો', safe_detected: 'સુરક્ષિત / ઓછી ગંભીરતાનું અવલોકન', violated_rule: 'ઉલ્લંઘન કરાયેલ નિયમ', required_action: 'જરૂરી કાર્યવાહી', stop_work: 'કામ બંધ કરો અને ભૌતિક બેરિયર ફરી સ્થાપિત કરો', field_scenarios: 'ફીલ્ડ સેફ્ટી પરિસ્થિતિઓ', safe_status: 'સુરક્ષિત / નિયંત્રિત', hse_dashboard: 'HSE સેફ્ટી ડેશબોર્ડ', management_dashboard: 'મેનેજમેન્ટ ડેશબોર્ડ', employee_dashboard: 'કર્મચારી ડેશબોર્ડ'
  },
  'ಕನ್ನಡ (Kannada)': {
    title: 'OIL-SIF ಕಮಾಂಡ್ ಹಬ್', subtitle: 'ಎಂಟರ್‌ಪ್ರೈಸ್ SIF ಪೂರ್ವಸೂಚಕ ಪತ್ತೆ ಮತ್ತು ಬಹುಭಾಷಾ ಬ್ಯಾರಿಯರ್ ಇಂಟೆಲಿಜೆನ್ಸ್ ಎಂಜಿನ್', welcome: 'ಸ್ವಾಗತ', logout: 'ಲಾಗ್ ಔಟ್ / ಲಾಗಿನ್‌ಗೆ ಹಿಂತಿರುಗಿ', select_lang: 'ಇಂಟರ್ಫೇಸ್ ಭಾಷೆ', field_worker: 'ಫೀಲ್ಡ್ ಕಾರ್ಮಿಕ', hse_officer: 'HSE ಅಧಿಕಾರಿ', management: 'ನಿರ್ವಹಣೆ', command_modules: 'ಕಮಾಂಡ್ ಮಾಡ್ಯೂಲ್‌ಗಳು', overview: 'ಅವಲೋಕನ', report_analysis: 'ವರದಿ ವಿಶ್ಲೇಷಣೆ', intelligence: 'ಇಂಟೆಲಿಜೆನ್ಸ್', ai_copilot: 'AI ಕೋ-ಪೈಲಟ್', my_dashboard: 'ನನ್ನ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್', facility_node: 'ಸೌಲಭ್ಯ ನೋಡ್', engine_telemetry: 'ಎಂಜಿನ್ ಟೆಲಿಮೆಟ್ರಿ', authorized_operator: 'ಅಧಿಕೃತ ಆಪರೇಟರ್', language: 'ಭಾಷೆ', role_protocol_active: 'ಪ್ರೋಟೋಕಾಲ್ ಸಕ್ರಿಯ', terminate_session: 'ಸೆಷನ್ ಅಂತ್ಯಗೊಳಿಸಿ', secure_credential_access: 'ಸುರಕ್ಷಿತ ಕ್ರೆಡೆನ್ಷಿಯಲ್ ಪ್ರವೇಶ', credential_required: 'ಕ್ರೆಡೆನ್ಷಿಯಲ್ ಅಗತ್ಯ', role_based_access: 'ಪಾತ್ರ ಆಧಾರಿತ ಪ್ರವೇಶ', authenticated_session: 'ದೃಢೀಕೃತ ಸೆಷನ್', sign_in: 'ಸೈನ್ ಇನ್', register_account: 'ಹೊಸ ಖಾತೆ ನೋಂದಣಿ', username: 'ಬಳಕೆದಾರ ಹೆಸರು', password: 'ಪಾಸ್‌ವರ್ಡ್', full_official_name: 'ಪೂರ್ಣ ಅಧಿಕೃತ ಹೆಸರು', new_username: 'ಹೊಸ ಬಳಕೆದಾರ ಹೆಸರು', new_password: 'ಹೊಸ ಪಾಸ್‌ವರ್ಡ್', designate_role: 'ಪಾತ್ರದ ಮಟ್ಟ ಆಯ್ಕೆ ಮಾಡಿ', authenticate_access: 'ಪ್ರವೇಶ ದೃಢೀಕರಿಸಿ', register_user: 'ಬಳಕೆದಾರರನ್ನು ನೋಂದಾಯಿಸಿ', authenticating: 'ದೃಢೀಕರಣ ನಡೆಯುತ್ತಿದೆ...', creating_account: 'ಖಾತೆ ರಚಿಸಲಾಗುತ್ತಿದೆ...', account_created: 'ಖಾತೆ ಯಶಸ್ವಿಯಾಗಿ ರಚಿಸಲಾಗಿದೆ. ಈಗ ಬಳಕೆದಾರ ಹೆಸರು ಮತ್ತು ಪಾಸ್‌ವರ್ಡ್ ಬಳಸಿ ಸೈನ್ ಇನ್ ಮಾಡಿ.', demo_credentials: 'ಡೆಮೋ ಕ್ರೆಡೆನ್ಷಿಯಲ್‌ಗಳು', global_fleet_barrier: 'ಗ್ಲೋಬಲ್ ಫ್ಲೀಟ್ ಬ್ಯಾರಿಯರ್ ಹೆಲ್ತ್ ಟೆಲಿಮೆಟ್ರಿ', login_required: 'ಮುಂದುವರಿಯಲು ದಯವಿಟ್ಟು ಸೈನ್ ಇನ್ ಮಾಡಿ.', invalid_credentials: 'ಬಳಕೆದಾರ ಹೆಸರು ಅಥವಾ ಪಾಸ್‌ವರ್ಡ್ ತಪ್ಪಾಗಿದೆ.', all_fields_required: 'ಎಲ್ಲಾ ಕ್ಷೇತ್ರಗಳು ಅಗತ್ಯ.', loading: 'ಲೋಡ್ ಆಗುತ್ತಿದೆ...', loading_intelligence: 'OIL-SIF ಇಂಟೆಲಿಜೆನ್ಸ್ ಲೋಡ್ ಆಗುತ್ತಿದೆ...', unable_load_dashboard: 'ಡ್ಯಾಶ್‌ಬೋರ್ಡ್ ಡೇಟಾ ಲೋಡ್ ಆಗಲಿಲ್ಲ.', total_reports: 'ಒಟ್ಟು ವರದಿಗಳು', sif_potential: 'SIF ಸಾಧ್ಯತೆ', high_sif_probability: 'ಹೆಚ್ಚಿನ SIF ಸಾಧ್ಯತೆ', awaiting_hse_review: 'HSE ಪರಿಶೀಲನೆ ಬಾಕಿ', reports_pending_validation: 'ಮಾನವ ಪರಿಶೀಲನೆಗಾಗಿ ಬಾಕಿ ಇರುವ ವರದಿಗಳು', sif_risk_overview: 'SIF ಅಪಾಯ ಅವಲೋಕನ', low_sif_probability: 'ಕಡಿಮೆ SIF ಸಾಧ್ಯತೆ', review_zone: 'ಪರಿಶೀಲನೆ ವಲಯ', high_probability_band: 'ಹೆಚ್ಚಿನ SIF ಸಾಧ್ಯತೆ', top_recurring_precursors: 'ಅತ್ಯಂತ ಪುನರಾವರ್ತಿತ ಪೂರ್ವಸೂಚಕಗಳು', recent_high_risk: 'ಇತ್ತೀಚಿನ ಹೆಚ್ಚಿನ ಅಪಾಯದ ವರದಿಗಳು', safety_report_explorer: 'ಸುರಕ್ಷತಾ ವರದಿ ಎಕ್ಸ್‌ಪ್ಲೋರರ್', search_placeholder: 'ವರದಿ ID, ಚಟುವಟಿಕೆ, ಪೂರ್ವಸೂಚಕ ಅಥವಾ ವರದಿ ಪಠ್ಯ ಹುಡುಕಿ...', all: 'ಎಲ್ಲಾ', pending_review: 'ಪರಿಶೀಲನೆ ಬಾಕಿ', selected_safety_report: 'ಆಯ್ದ ಸುರಕ್ಷತಾ ವರದಿ', run_ai_analysis: 'AI SIF ವಿಶ್ಲೇಷಣೆ ಚಲಾಯಿಸಿ', analyzing_report: 'ವರದಿ ವಿಶ್ಲೇಷಣೆ ನಡೆಯುತ್ತಿದೆ...', ai_analysis_result: 'AI ವಿಶ್ಲೇಷಣೆ ಫಲಿತಾಂಶ', precursor_intelligence: 'ಪೂರ್ವಸೂಚಕ ಇಂಟೆಲಿಜೆನ್ಸ್', barrier_analysis: 'ಬ್ಯಾರಿಯರ್ ವಿಶ್ಲೇಷಣೆ', life_saving_rules: 'Life-Saving Rules', activity_risk: 'ಚಟುವಟಿಕೆ ಅಪಾಯ', hse_review_queue: 'HSE ಪರಿಶೀಲನಾ ಸರತಿ', review: 'ಪರಿಶೀಲನೆ', ai_safety_copilot: 'AI ಸುರಕ್ಷತಾ ಕೋ-ಪೈಲಟ್', suggested_questions: 'ಸೂಚಿಸಿದ ಪ್ರಶ್ನೆಗಳು', quick_queries: 'ಸಾಮಾನ್ಯ ಸುರಕ್ಷತಾ-ಇಂಟೆಲಿಜೆನ್ಸ್ ಕಾರ್ಯಗಳಿಗೆ ತ್ವರಿತ ಪ್ರಶ್ನೆಗಳು', dataset_grounded_assistant: 'ಡೇಟಾಸೆಟ್ ಆಧಾರಿತ ಸುರಕ್ಷತಾ ಇಂಟೆಲಿಜೆನ್ಸ್ ಸಹಾಯಕ', analyzing_safety: 'ಸುರಕ್ಷತಾ ಇಂಟೆಲಿಜೆನ್ಸ್ ವಿಶ್ಲೇಷಿಸಲಾಗುತ್ತಿದೆ...', ask_copilot: 'OIL-SIF Copilot ಅನ್ನು ಕೇಳಿ...', send: 'ಕಳುಹಿಸಿ →', hse_validation_notice: 'HSE ಪರಿಶೀಲನೆ ಸೂಚನೆ', incident_hazard_scanner: 'ಘಟನೆ ಮತ್ತು ಅಪಾಯ ಪೂರ್ವಸೂಚಕ ಸ್ಕ್ಯಾನರ್', describe_hazard: 'ಗಮನಿಸಿದ ಅಸುರಕ್ಷಿತ ಸ್ಥಿತಿ ಅಥವಾ ಸಮೀಪದ ಅಪಘಾತವನ್ನು ವಿವರಿಸಿ:', scan_btn: 'AI Guard ಮೂಲಕ ಅಪಾಯ ಸ್ಕ್ಯಾನ್ ಮಾಡಿ', critical_detected: 'ಗಂಭೀರ SIF ಪೂರ್ವಸೂಚಕ ಪತ್ತೆಯಾಗಿದೆ', safe_detected: 'ಸುರಕ್ಷಿತ / ಕಡಿಮೆ-ಗಂಭೀರ ಅವಲೋಕನ', violated_rule: 'ಉಲ್ಲಂಘಿಸಿದ ನಿಯಮ', required_action: 'ಅಗತ್ಯ ಕ್ರಮ', stop_work: 'ಕೆಲಸ ನಿಲ್ಲಿಸಿ ಮತ್ತು ಭೌತಿಕ ಬ್ಯಾರಿಯರ್ ಮರುಸ್ಥಾಪಿಸಿ', field_scenarios: 'ಫೀಲ್ಡ್ ಸುರಕ್ಷತಾ ಪರಿಸ್ಥಿತಿಗಳು', safe_status: 'ಸುರಕ್ಷಿತ / ನಿಯಂತ್ರಿತ', hse_dashboard: 'HSE ಸುರಕ್ಷತಾ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್', management_dashboard: 'ನಿರ್ವಹಣಾ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್', employee_dashboard: 'ಉದ್ಯೋಗಿ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್'
  },
  'മലയാളം (Malayalam)': {
    title: 'OIL-SIF കമാൻഡ് ഹബ്', subtitle: 'എന്റർപ്രൈസ് SIF മുൻസൂചക കണ്ടെത്തലും ബഹുഭാഷാ ബാരിയർ ഇന്റലിജൻസ് എഞ്ചിനും', welcome: 'സ്വാഗതം', logout: 'ലോഗ് ഔട്ട് / ലോഗിനിലേക്ക് മടങ്ങുക', select_lang: 'ഇന്റർഫേസ് ഭാഷ', field_worker: 'ഫീൽഡ് തൊഴിലാളി', hse_officer: 'HSE ഉദ്യോഗസ്ഥൻ', management: 'മാനേജ്മെന്റ്', command_modules: 'കമാൻഡ് മോഡ്യൂളുകൾ', overview: 'അവലോകനം', report_analysis: 'റിപ്പോർട്ട് വിശകലനം', intelligence: 'ഇന്റലിജൻസ്', ai_copilot: 'AI കോ-പൈലറ്റ്', my_dashboard: 'എന്റെ ഡാഷ്ബോർഡ്', facility_node: 'ഫസിലിറ്റി നോഡ്', engine_telemetry: 'എഞ്ചിൻ ടെലിമെട്രി', authorized_operator: 'അധികൃത ഓപ്പറേറ്റർ', language: 'ഭാഷ', role_protocol_active: 'പ്രോട്ടോക്കോൾ സജീവം', terminate_session: 'സെഷൻ അവസാനിപ്പിക്കുക', secure_credential_access: 'സുരക്ഷിത ക്രെഡൻഷ്യൽ ആക്സസ്', credential_required: 'ക്രെഡൻഷ്യൽ ആവശ്യമാണ്', role_based_access: 'റോൾ അടിസ്ഥാനമാക്കിയുള്ള ആക്സസ്', authenticated_session: 'സ്ഥിരീകരിച്ച സെഷൻ', sign_in: 'സൈൻ ഇൻ', register_account: 'പുതിയ അക്കൗണ്ട് രജിസ്റ്റർ ചെയ്യുക', username: 'ഉപയോക്തൃനാമം', password: 'പാസ്‌വേഡ്', full_official_name: 'പൂർണ്ണ ഔദ്യോഗിക പേര്', new_username: 'പുതിയ ഉപയോക്തൃനാമം', new_password: 'പുതിയ പാസ്‌വേഡ്', designate_role: 'റോൾ നില തിരഞ്ഞെടുക്കുക', authenticate_access: 'ആക്സസ് സ്ഥിരീകരിക്കുക', register_user: 'ഉപയോക്താവിനെ രജിസ്റ്റർ ചെയ്യുക', authenticating: 'സ്ഥിരീകരിക്കുന്നു...', creating_account: 'അക്കൗണ്ട് സൃഷ്ടിക്കുന്നു...', account_created: 'അക്കൗണ്ട് വിജയകരമായി സൃഷ്ടിച്ചു. ഇപ്പോൾ ഉപയോക്തൃനാമവും പാസ്‌വേഡും ഉപയോഗിച്ച് സൈൻ ഇൻ ചെയ്യാം.', demo_credentials: 'ഡെമോ ക്രെഡൻഷ്യലുകൾ', global_fleet_barrier: 'ഗ്ലോബൽ ഫ്ലീറ്റ് ബാരിയർ ഹെൽത്ത് ടെലിമെട്രി', login_required: 'തുടരാൻ സൈൻ ഇൻ ചെയ്യുക.', invalid_credentials: 'ഉപയോക്തൃനാമമോ പാസ്‌വേഡോ തെറ്റാണ്.', all_fields_required: 'എല്ലാ ഫീൽഡുകളും ആവശ്യമാണ്.', loading: 'ലോഡ് ചെയ്യുന്നു...', loading_intelligence: 'OIL-SIF ഇന്റലിജൻസ് ലോഡ് ചെയ്യുന്നു...', unable_load_dashboard: 'ഡാഷ്ബോർഡ് ഡാറ്റ ലോഡ് ചെയ്യാനായില്ല.', total_reports: 'മൊത്തം റിപ്പോർട്ടുകൾ', sif_potential: 'SIF സാധ്യത', high_sif_probability: 'ഉയർന്ന SIF സാധ്യത', awaiting_hse_review: 'HSE അവലോകനം കാത്തിരിക്കുന്നു', reports_pending_validation: 'മാനുഷിക പരിശോധന കാത്തിരിക്കുന്ന റിപ്പോർട്ടുകൾ', sif_risk_overview: 'SIF അപകട അവലോകനം', low_sif_probability: 'കുറഞ്ഞ SIF സാധ്യത', review_zone: 'അവലോകന മേഖല', high_probability_band: 'ഉയർന്ന SIF സാധ്യത', top_recurring_precursors: 'പ്രധാന ആവർത്തിക്കുന്ന മുൻസൂചകങ്ങൾ', recent_high_risk: 'സമീപകാല ഉയർന്ന അപകട റിപ്പോർട്ടുകൾ', safety_report_explorer: 'സേഫ്റ്റി റിപ്പോർട്ട് എക്സ്പ്ലോറർ', search_placeholder: 'റിപ്പോർട്ട് ID, പ്രവർത്തനം, മുൻസൂചകം അല്ലെങ്കിൽ റിപ്പോർട്ട് ടെക്സ്റ്റ് തിരയുക...', all: 'എല്ലാം', pending_review: 'അവലോകനം കാത്തിരിക്കുന്നു', selected_safety_report: 'തിരഞ്ഞെടുത്ത സുരക്ഷാ റിപ്പോർട്ട്', run_ai_analysis: 'AI SIF വിശകലനം നടത്തുക', analyzing_report: 'റിപ്പോർട്ട് വിശകലനം ചെയ്യുന്നു...', ai_analysis_result: 'AI വിശകലന ഫലം', precursor_intelligence: 'മുൻസൂചക ഇന്റലിജൻസ്', barrier_analysis: 'ബാരിയർ വിശകലനം', life_saving_rules: 'Life-Saving Rules', activity_risk: 'പ്രവർത്തന അപകടം', hse_review_queue: 'HSE അവലോകന ക്യൂ', review: 'അവലോകനം', ai_safety_copilot: 'AI സേഫ്റ്റി കോ-പൈലറ്റ്', suggested_questions: 'നിർദ്ദേശിച്ച ചോദ്യങ്ങൾ', quick_queries: 'സാധാരണ സേഫ്റ്റി-ഇന്റലിജൻസ് ജോലികൾക്കുള്ള ദ്രുത ചോദ്യങ്ങൾ', dataset_grounded_assistant: 'ഡാറ്റാസെറ്റ് അടിസ്ഥാനമാക്കിയ സുരക്ഷാ ഇന്റലിജൻസ് സഹായി', analyzing_safety: 'സുരക്ഷാ ഇന്റലിജൻസ് വിശകലനം ചെയ്യുന്നു...', ask_copilot: 'OIL-SIF Copilotനോട് ചോദിക്കുക...', send: 'അയയ്ക്കുക →', hse_validation_notice: 'HSE പരിശോധനാ അറിയിപ്പ്', incident_hazard_scanner: 'സംഭവവും അപകട മുൻസൂചക സ്കാനറും', describe_hazard: 'കണ്ട അസുരക്ഷിത അവസ്ഥയോ near miss-ഓ വിവരിക്കുക:', scan_btn: 'AI Guard ഉപയോഗിച്ച് അപകടം സ്കാൻ ചെയ്യുക', critical_detected: 'ഗുരുതര SIF മുൻസൂചകം കണ്ടെത്തി', safe_detected: 'സുരക്ഷിതം / കുറഞ്ഞ ഗുരുതരതയുള്ള നിരീക്ഷണം', violated_rule: 'ലംഘിച്ച നിയമം', required_action: 'ആവശ്യമായ നടപടി', stop_work: 'ജോലി നിർത്തി ഭൗതിക ബാരിയർ പുനഃസ്ഥാപിക്കുക', field_scenarios: 'ഫീൽഡ് സുരക്ഷാ സാഹചര്യങ്ങൾ', safe_status: 'സുരക്ഷിതം / നിയന്ത്രിതം', hse_dashboard: 'HSE സുരക്ഷാ ഡാഷ്ബോർഡ്', management_dashboard: 'മാനേജ്മെന്റ് ഡാഷ്ബോർഡ്', employee_dashboard: 'ജീവനക്കാരുടെ ഡാഷ്ബോർഡ്'
  },
  'मराठी (Marathi)': {
    title: 'OIL-SIF कमांड हब', subtitle: 'एंटरप्राइज SIF पूर्वसूचक शोध आणि बहुभाषिक बॅरियर इंटेलिजन्स इंजिन', welcome: 'स्वागत आहे', logout: 'लॉग आउट / लॉगिनवर परत जा', select_lang: 'इंटरफेस भाषा', field_worker: 'फील्ड कर्मचारी', hse_officer: 'HSE अधिकारी', management: 'व्यवस्थापन', command_modules: 'कमांड मॉड्यूल्स', overview: 'आढावा', report_analysis: 'अहवाल विश्लेषण', intelligence: 'इंटेलिजन्स', ai_copilot: 'AI को-पायलट', my_dashboard: 'माझे डॅशबोर्ड', facility_node: 'फॅसिलिटी नोड', engine_telemetry: 'इंजिन टेलिमेट्री', authorized_operator: 'अधिकृत ऑपरेटर', language: 'भाषा', role_protocol_active: 'प्रोटोकॉल सक्रिय', terminate_session: 'सत्र समाप्त करा', secure_credential_access: 'सुरक्षित क्रेडेन्शियल प्रवेश', credential_required: 'क्रेडेन्शियल आवश्यक', role_based_access: 'भूमिकेवर आधारित प्रवेश', authenticated_session: 'प्रमाणित सत्र', sign_in: 'साइन इन', register_account: 'नवीन खाते नोंदणी करा', username: 'वापरकर्ता नाव', password: 'पासवर्ड', full_official_name: 'पूर्ण अधिकृत नाव', new_username: 'नवीन वापरकर्ता नाव', new_password: 'नवीन पासवर्ड', designate_role: 'भूमिका स्तर निवडा', authenticate_access: 'प्रवेश प्रमाणित करा', register_user: 'वापरकर्ता नोंदणी करा', authenticating: 'प्रमाणीकरण सुरू आहे...', creating_account: 'खाते तयार होत आहे...', account_created: 'खाते यशस्वीरित्या तयार झाले. आता वापरकर्ता नाव आणि पासवर्डने साइन इन करू शकता.', demo_credentials: 'डेमो क्रेडेन्शियल्स', global_fleet_barrier: 'ग्लोबल फ्लीट बॅरियर हेल्थ टेलिमेट्री', login_required: 'पुढे जाण्यासाठी कृपया साइन इन करा.', invalid_credentials: 'वापरकर्ता नाव किंवा पासवर्ड चुकीचा आहे.', all_fields_required: 'सर्व फील्ड आवश्यक आहेत.', loading: 'लोड होत आहे...', loading_intelligence: 'OIL-SIF इंटेलिजन्स लोड होत आहे...', unable_load_dashboard: 'डॅशबोर्ड डेटा लोड करता आला नाही.', total_reports: 'एकूण अहवाल', sif_potential: 'SIF संभाव्यता', high_sif_probability: 'उच्च SIF संभाव्यता', awaiting_hse_review: 'HSE पुनरावलोकन प्रलंबित', reports_pending_validation: 'मानवी पडताळणी प्रलंबित अहवाल', sif_risk_overview: 'SIF जोखीम आढावा', low_sif_probability: 'कमी SIF संभाव्यता', review_zone: 'पुनरावलोकन क्षेत्र', high_probability_band: 'उच्च SIF संभाव्यता', top_recurring_precursors: 'सर्वाधिक पुनरावृत्ती होणारे पूर्वसूचक', recent_high_risk: 'अलीकडील उच्च-जोखीम अहवाल', safety_report_explorer: 'सुरक्षा अहवाल एक्सप्लोरर', search_placeholder: 'अहवाल ID, क्रियाकलाप, पूर्वसूचक किंवा अहवाल मजकूर शोधा...', all: 'सर्व', pending_review: 'पुनरावलोकन प्रलंबित', selected_safety_report: 'निवडलेला सुरक्षा अहवाल', run_ai_analysis: 'AI SIF विश्लेषण चालवा', analyzing_report: 'अहवाल विश्लेषण सुरू आहे...', ai_analysis_result: 'AI विश्लेषण निकाल', precursor_intelligence: 'पूर्वसूचक इंटेलिजन्स', barrier_analysis: 'बॅरियर विश्लेषण', life_saving_rules: 'Life-Saving Rules', activity_risk: 'क्रियाकलाप जोखीम', hse_review_queue: 'HSE पुनरावलोकन रांग', review: 'पुनरावलोकन', ai_safety_copilot: 'AI सुरक्षा को-पायलट', suggested_questions: 'सुचवलेले प्रश्न', quick_queries: 'सामान्य सुरक्षा-इंटेलिजन्स कामांसाठी झटपट प्रश्न', dataset_grounded_assistant: 'डेटासेट-आधारित सुरक्षा इंटेलिजन्स सहाय्यक', analyzing_safety: 'सुरक्षा इंटेलिजन्सचे विश्लेषण सुरू आहे...', ask_copilot: 'OIL-SIF Copilot ला विचारा...', send: 'पाठवा →', hse_validation_notice: 'HSE पडताळणी सूचना', incident_hazard_scanner: 'घटना आणि धोका पूर्वसूचक स्कॅनर', describe_hazard: 'दिसलेली असुरक्षित स्थिती किंवा near miss चे वर्णन करा:', scan_btn: 'AI Guard ने धोका स्कॅन करा', critical_detected: 'गंभीर SIF पूर्वसूचक आढळला', safe_detected: 'सुरक्षित / कमी-गंभीर निरीक्षण', violated_rule: 'उल्लंघन केलेला नियम', required_action: 'आवश्यक कृती', stop_work: 'काम थांबवा आणि भौतिक बॅरियर पुन्हा स्थापित करा', field_scenarios: 'फील्ड सुरक्षा परिस्थिती', safe_status: 'सुरक्षित / नियंत्रित', hse_dashboard: 'HSE सुरक्षा डॅशबोर्ड', management_dashboard: 'व्यवस्थापन डॅशबोर्ड', employee_dashboard: 'कर्मचारी डॅशबोर्ड'
  },
  'ଓଡ଼ିଆ (Odia)': {
    title: 'OIL-SIF କମାଣ୍ଡ ହବ୍', subtitle: 'ଏଣ୍ଟରପ୍ରାଇଜ୍ SIF ପୂର୍ବସୂଚକ ଚିହ୍ନଟ ଏବଂ ବହୁଭାଷୀ ବ୍ୟାରିଅର ଇଣ୍ଟେଲିଜେନ୍ସ ଇଞ୍ଜିନ', welcome: 'ସ୍ୱାଗତ', logout: 'ଲଗ ଆଉଟ / ଲଗଇନକୁ ଫେରନ୍ତୁ', select_lang: 'ଇଣ୍ଟରଫେସ ଭାଷା', field_worker: 'ଫିଲ୍ଡ କର୍ମଚାରୀ', hse_officer: 'HSE ଅଧିକାରୀ', management: 'ପରିଚାଳନା', command_modules: 'କମାଣ୍ଡ ମଡ୍ୟୁଲ', overview: 'ସାରାଂଶ', report_analysis: 'ରିପୋର୍ଟ ବିଶ୍ଳେଷଣ', intelligence: 'ଇଣ୍ଟେଲିଜେନ୍ସ', ai_copilot: 'AI କୋ-ପାଇଲଟ', my_dashboard: 'ମୋ ଡ୍ୟାସବୋର୍ଡ', facility_node: 'ଫାସିଲିଟି ନୋଡ', engine_telemetry: 'ଇଞ୍ଜିନ ଟେଲିମେଟ୍ରି', authorized_operator: 'ଅନୁମୋଦିତ ଅପରେଟର', language: 'ଭାଷା', role_protocol_active: 'ପ୍ରୋଟୋକଲ ସକ୍ରିୟ', terminate_session: 'ସେସନ ସମାପ୍ତ କରନ୍ତୁ', secure_credential_access: 'ସୁରକ୍ଷିତ କ୍ରେଡେନ୍ସିଆଲ ଆକ୍ସେସ', credential_required: 'କ୍ରେଡେନ୍ସିଆଲ ଆବଶ୍ୟକ', role_based_access: 'ଭୂମିକା ଆଧାରିତ ଆକ୍ସେସ', authenticated_session: 'ପ୍ରମାଣିତ ସେସନ', sign_in: 'ସାଇନ ଇନ', register_account: 'ନୂଆ ଖାତା ପଞ୍ଜିକରଣ', username: 'ବ୍ୟବହାରକାରୀ ନାମ', password: 'ପାସୱାର୍ଡ', full_official_name: 'ସମ୍ପୂର୍ଣ୍ଣ ସରକାରୀ ନାମ', new_username: 'ନୂଆ ବ୍ୟବହାରକାରୀ ନାମ', new_password: 'ନୂଆ ପାସୱାର୍ଡ', designate_role: 'ଭୂମିକା ସ୍ତର ବାଛନ୍ତୁ', authenticate_access: 'ଆକ୍ସେସ ପ୍ରମାଣିତ କରନ୍ତୁ', register_user: 'ବ୍ୟବହାରକାରୀ ପଞ୍ଜିକରଣ କରନ୍ତୁ', authenticating: 'ପ୍ରମାଣୀକରଣ ଚାଲିଛି...', creating_account: 'ଖାତା ତିଆରି ହେଉଛି...', account_created: 'ଖାତା ସଫଳତାର ସହିତ ତିଆରି ହୋଇଛି। ଏବେ ବ୍ୟବହାରକାରୀ ନାମ ଏବଂ ପାସୱାର୍ଡରେ ସାଇନ ଇନ କରନ୍ତୁ।', demo_credentials: 'ଡେମୋ କ୍ରେଡେନ୍ସିଆଲ', global_fleet_barrier: 'ଗ୍ଲୋବାଲ ଫ୍ଲିଟ ବ୍ୟାରିଅର ହେଲ୍ଥ ଟେଲିମେଟ୍ରି', login_required: 'ଆଗକୁ ବଢିବା ପାଇଁ ସାଇନ ଇନ କରନ୍ତୁ।', invalid_credentials: 'ବ୍ୟବହାରକାରୀ ନାମ କିମ୍ବା ପାସୱାର୍ଡ ଭୁଲ।', all_fields_required: 'ସମସ୍ତ ଫିଲ୍ଡ ଆବଶ୍ୟକ।', loading: 'ଲୋଡ ହେଉଛି...', total_reports: 'ମୋଟ ରିପୋର୍ଟ', sif_potential: 'SIF ସମ୍ଭାବନା', high_sif_probability: 'ଉଚ୍ଚ SIF ସମ୍ଭାବନା', awaiting_hse_review: 'HSE ସମୀକ୍ଷା ପ୍ରତୀକ୍ଷାରତ', reports_pending_validation: 'ମାନବ ଯାଞ୍ଚ ପାଇଁ ପ୍ରତୀକ୍ଷାରତ ରିପୋର୍ଟ', sif_risk_overview: 'SIF ଝୁମ୍ପ ସାରାଂଶ', low_sif_probability: 'କମ SIF ସମ୍ଭାବନା', review_zone: 'ସମୀକ୍ଷା ଅଞ୍ଚଳ', high_probability_band: 'ଉଚ୍ଚ SIF ସମ୍ଭାବନା', top_recurring_precursors: 'ଶୀର୍ଷ ପୁନରାବୃତ ପୂର୍ବସୂଚକ', recent_high_risk: 'ସମ୍ପ୍ରତିର ଉଚ୍ଚ-ଝୁମ୍ପ ରିପୋର୍ଟ', safety_report_explorer: 'ସୁରକ୍ଷା ରିପୋର୍ଟ ଏକ୍ସପ୍ଲୋରର', search_placeholder: 'ରିପୋର୍ଟ ID, କାର୍ଯ୍ୟ, ପୂର୍ବସୂଚକ କିମ୍ବା ରିପୋର୍ଟ ଟେକ୍ସଟ ଖୋଜନ୍ତୁ...', all: 'ସମସ୍ତ', pending_review: 'ସମୀକ୍ଷା ପ୍ରତୀକ୍ଷାରତ', selected_safety_report: 'ଚୟନିତ ସୁରକ୍ଷା ରିପୋର୍ଟ', run_ai_analysis: 'AI SIF ବିଶ୍ଳେଷଣ ଚଲାନ୍ତୁ', analyzing_report: 'ରିପୋର୍ଟ ବିଶ୍ଳେଷଣ ଚାଲିଛି...', ai_analysis_result: 'AI ବିଶ୍ଳେଷଣ ଫଳାଫଳ', precursor_intelligence: 'ପୂର୍ବସୂଚକ ଇଣ୍ଟେଲିଜେନ୍ସ', barrier_analysis: 'ବ୍ୟାରିଅର ବିଶ୍ଳେଷଣ', life_saving_rules: 'Life-Saving Rules', activity_risk: 'କାର୍ଯ୍ୟ ଝୁମ୍ପ', hse_review_queue: 'HSE ସମୀକ୍ଷା କ୍ୟୁ', review: 'ସମୀକ୍ଷା', ai_safety_copilot: 'AI ସୁରକ୍ଷା କୋ-ପାଇଲଟ', suggested_questions: 'ପ୍ରସ୍ତାବିତ ପ୍ରଶ୍ନ', quick_queries: 'ସାଧାରଣ ସୁରକ୍ଷା-ଇଣ୍ଟେଲିଜେନ୍ସ କାମ ପାଇଁ ତ୍ୱରିତ ପ୍ରଶ୍ନ', dataset_grounded_assistant: 'ଡାଟାସେଟ ଆଧାରିତ ସୁରକ୍ଷା ଇଣ୍ଟେଲିଜେନ୍ସ ସହାୟକ', analyzing_safety: 'ସୁରକ୍ଷା ଇଣ୍ଟେଲିଜେନ୍ସ ବିଶ୍ଳେଷଣ ହେଉଛି...', ask_copilot: 'OIL-SIF Copilotକୁ ପଚାରନ୍ତୁ...', send: 'ପଠାନ୍ତୁ →', hse_validation_notice: 'HSE ଯାଞ୍ଚ ସୂଚନା', incident_hazard_scanner: 'ଘଟଣା ଏବଂ ବିପଦ ପୂର୍ବସୂଚକ ସ୍କାନର', describe_hazard: 'ଦେଖାଯାଇଥିବା ଅସୁରକ୍ଷିତ ଅବସ୍ଥା କିମ୍ବା near miss ବିଷୟରେ ଲେଖନ୍ତୁ:', scan_btn: 'AI Guard ସହିତ ବିପଦ ସ୍କାନ କରନ୍ତୁ', critical_detected: 'ଗୁରୁତର SIF ପୂର୍ବସୂଚକ ଚିହ୍ନଟ ହୋଇଛି', safe_detected: 'ନିରାପଦ / କମ-ଗୁରୁତର ପର୍ଯ୍ୟବେକ୍ଷଣ', violated_rule: 'ଉଲ୍ଲଂଘିତ ନିୟମ', required_action: 'ଆବଶ୍ୟକ କାର୍ଯ୍ୟ', stop_work: 'କାମ ବନ୍ଦ କରନ୍ତୁ ଏବଂ ଭୌତିକ ବ୍ୟାରିଅର ପୁନଃସ୍ଥାପନ କରନ୍ତୁ', field_scenarios: 'ଫିଲ୍ଡ ସୁରକ୍ଷା ପରିସ୍ଥିତି', safe_status: 'ନିରାପଦ / ନିୟନ୍ତ୍ରିତ', hse_dashboard: 'HSE ସୁରକ୍ଷା ଡ୍ୟାସବୋର୍ଡ', management_dashboard: 'ପରିଚାଳନା ଡ୍ୟାସବୋର୍ଡ', employee_dashboard: 'କର୍ମଚାରୀ ଡ୍ୟାସବୋର୍ଡ'
  },
  'ਪੰਜਾਬੀ (Punjabi)': {
    title: 'OIL-SIF ਕਮਾਂਡ ਹੱਬ', subtitle: 'ਐਂਟਰਪ੍ਰਾਈਜ਼ SIF ਪੂਰਵ-ਸੂਚਕ ਪਛਾਣ ਅਤੇ ਬਹੁਭਾਸ਼ੀ ਬੈਰੀਅਰ ਇੰਟੈਲੀਜੈਂਸ ਇੰਜਣ', welcome: 'ਜੀ ਆਇਆਂ ਨੂੰ', logout: 'ਲੌਗ ਆਉਟ / ਲੌਗਇਨ ਵੱਲ ਵਾਪਸ ਜਾਓ', select_lang: 'ਇੰਟਰਫੇਸ ਭਾਸ਼ਾ', field_worker: 'ਫੀਲਡ ਕਰਮਚਾਰੀ', hse_officer: 'HSE ਅਧਿਕਾਰੀ', management: 'ਪ੍ਰਬੰਧਨ', command_modules: 'ਕਮਾਂਡ ਮੋਡੀਊਲ', overview: 'ਸੰਖੇਪ', report_analysis: 'ਰਿਪੋਰਟ ਵਿਸ਼ਲੇਸ਼ਣ', intelligence: 'ਇੰਟੈਲੀਜੈਂਸ', ai_copilot: 'AI ਕੋ-ਪਾਇਲਟ', my_dashboard: 'ਮੇਰਾ ਡੈਸ਼ਬੋਰਡ', facility_node: 'ਫੈਸਿਲਟੀ ਨੋਡ', engine_telemetry: 'ਇੰਜਣ ਟੈਲੀਮੇਟਰੀ', authorized_operator: 'ਅਧਿਕਾਰਤ ਓਪਰੇਟਰ', language: 'ਭਾਸ਼ਾ', role_protocol_active: 'ਪ੍ਰੋਟੋਕੋਲ ਸਰਗਰਮ', terminate_session: 'ਸੈਸ਼ਨ ਸਮਾਪਤ ਕਰੋ', secure_credential_access: 'ਸੁਰੱਖਿਅਤ ਕ੍ਰੈਡੈਂਸ਼ੀਅਲ ਐਕਸੈਸ', credential_required: 'ਕ੍ਰੈਡੈਂਸ਼ੀਅਲ ਲੋੜੀਂਦੇ', role_based_access: 'ਭੂਮਿਕਾ-ਆਧਾਰਿਤ ਐਕਸੈਸ', authenticated_session: 'ਪ੍ਰਮਾਣਿਤ ਸੈਸ਼ਨ', sign_in: 'ਸਾਈਨ ਇਨ', register_account: 'ਨਵਾਂ ਖਾਤਾ ਰਜਿਸਟਰ ਕਰੋ', username: 'ਯੂਜ਼ਰਨੇਮ', password: 'ਪਾਸਵਰਡ', full_official_name: 'ਪੂਰਾ ਅਧਿਕਾਰਕ ਨਾਮ', new_username: 'ਨਵਾਂ ਯੂਜ਼ਰਨੇਮ', new_password: 'ਨਵਾਂ ਪਾਸਵਰਡ', designate_role: 'ਭੂਮਿਕਾ ਪੱਧਰ ਚੁਣੋ', authenticate_access: 'ਐਕਸੈਸ ਪ੍ਰਮਾਣਿਤ ਕਰੋ', register_user: 'ਯੂਜ਼ਰ ਰਜਿਸਟਰ ਕਰੋ', authenticating: 'ਪ੍ਰਮਾਣਿਕਤਾ ਹੋ ਰਹੀ ਹੈ...', creating_account: 'ਖਾਤਾ ਬਣਾਇਆ ਜਾ ਰਿਹਾ ਹੈ...', account_created: 'ਖਾਤਾ ਸਫਲਤਾਪੂਰਵਕ ਬਣ ਗਿਆ। ਹੁਣ ਯੂਜ਼ਰਨੇਮ ਅਤੇ ਪਾਸਵਰਡ ਨਾਲ ਸਾਈਨ ਇਨ ਕਰੋ।', demo_credentials: 'ਡੈਮੋ ਕ੍ਰੈਡੈਂਸ਼ੀਅਲ', global_fleet_barrier: 'ਗਲੋਬਲ ਫਲੀਟ ਬੈਰੀਅਰ ਹੈਲਥ ਟੈਲੀਮੇਟਰੀ', login_required: 'ਜਾਰੀ ਰੱਖਣ ਲਈ ਸਾਈਨ ਇਨ ਕਰੋ।', invalid_credentials: 'ਯੂਜ਼ਰਨੇਮ ਜਾਂ ਪਾਸਵਰਡ ਗਲਤ ਹੈ।', all_fields_required: 'ਸਾਰੇ ਫੀਲਡ ਲੋੜੀਂਦੇ ਹਨ।', loading: 'ਲੋਡ ਹੋ ਰਿਹਾ ਹੈ...', loading_intelligence: 'OIL-SIF ਇੰਟੈਲੀਜੈਂਸ ਲੋਡ ਹੋ ਰਹੀ ਹੈ...', unable_load_dashboard: 'ਡੈਸ਼ਬੋਰਡ ਡਾਟਾ ਲੋਡ ਨਹੀਂ ਹੋਇਆ।', total_reports: 'ਕੁੱਲ ਰਿਪੋਰਟਾਂ', sif_potential: 'SIF ਸੰਭਾਵਨਾ', high_sif_probability: 'ਉੱਚ SIF ਸੰਭਾਵਨਾ', awaiting_hse_review: 'HSE ਸਮੀਖਿਆ ਬਕਾਇਆ', reports_pending_validation: 'ਮਾਨਵੀ ਜਾਂਚ ਲਈ ਬਕਾਇਆ ਰਿਪੋਰਟਾਂ', sif_risk_overview: 'SIF ਜੋਖਮ ਸੰਖੇਪ', low_sif_probability: 'ਘੱਟ SIF ਸੰਭਾਵਨਾ', review_zone: 'ਸਮੀਖਿਆ ਖੇਤਰ', high_probability_band: 'ਉੱਚ SIF ਸੰਭਾਵਨਾ', top_recurring_precursors: 'ਸਿਖਰ ਦੇ ਦੁਹਰਾਉਂਦੇ ਪੂਰਵ-ਸੂਚਕ', recent_high_risk: 'ਹਾਲੀਆ ਉੱਚ-ਜੋਖਮ ਰਿਪੋਰਟਾਂ', safety_report_explorer: 'ਸੇਫਟੀ ਰਿਪੋਰਟ ਐਕਸਪਲੋਰਰ', search_placeholder: 'ਰਿਪੋਰਟ ID, ਗਤੀਵਿਧੀ, ਪੂਰਵ-ਸੂਚਕ ਜਾਂ ਰਿਪੋਰਟ ਟੈਕਸਟ ਲੱਭੋ...', all: 'ਸਭ', pending_review: 'ਸਮੀਖਿਆ ਬਕਾਇਆ', selected_safety_report: 'ਚੁਣੀ ਹੋਈ ਸੁਰੱਖਿਆ ਰਿਪੋਰਟ', run_ai_analysis: 'AI SIF ਵਿਸ਼ਲੇਸ਼ਣ ਚਲਾਓ', analyzing_report: 'ਰਿਪੋਰਟ ਦਾ ਵਿਸ਼ਲੇਸ਼ਣ ਹੋ ਰਿਹਾ ਹੈ...', ai_analysis_result: 'AI ਵਿਸ਼ਲੇਸ਼ਣ ਨਤੀਜਾ', precursor_intelligence: 'ਪੂਰਵ-ਸੂਚਕ ਇੰਟੈਲੀਜੈਂਸ', barrier_analysis: 'ਬੈਰੀਅਰ ਵਿਸ਼ਲੇਸ਼ਣ', life_saving_rules: 'Life-Saving Rules', activity_risk: 'ਗਤੀਵਿਧੀ ਜੋਖਮ', hse_review_queue: 'HSE ਸਮੀਖਿਆ ਕਿਊ', review: 'ਸਮੀਖਿਆ', ai_safety_copilot: 'AI ਸੇਫਟੀ ਕੋ-ਪਾਇਲਟ', suggested_questions: 'ਸੁਝਾਏ ਸਵਾਲ', quick_queries: 'ਆਮ ਸੇਫਟੀ-ਇੰਟੈਲੀਜੈਂਸ ਕੰਮਾਂ ਲਈ ਤੇਜ਼ ਸਵਾਲ', dataset_grounded_assistant: 'ਡਾਟਾਸੈਟ-ਅਧਾਰਿਤ ਸੁਰੱਖਿਆ ਇੰਟੈਲੀਜੈਂਸ ਸਹਾਇਕ', analyzing_safety: 'ਸੁਰੱਖਿਆ ਇੰਟੈਲੀਜੈਂਸ ਦਾ ਵਿਸ਼ਲੇਸ਼ਣ ਹੋ ਰਿਹਾ ਹੈ...', ask_copilot: 'OIL-SIF Copilot ਨੂੰ ਪੁੱਛੋ...', send: 'ਭੇਜੋ →', hse_validation_notice: 'HSE ਜਾਂਚ ਸੂਚਨਾ', incident_hazard_scanner: 'ਘਟਨਾ ਅਤੇ ਖਤਰਾ ਪੂਰਵ-ਸੂਚਕ ਸਕੈਨਰ', describe_hazard: 'ਦੇਖੀ ਅਸੁਰੱਖਿਅਤ ਸਥਿਤੀ ਜਾਂ near miss ਬਾਰੇ ਦੱਸੋ:', scan_btn: 'AI Guard ਨਾਲ ਖਤਰਾ ਸਕੈਨ ਕਰੋ', critical_detected: 'ਗੰਭੀਰ SIF ਪੂਰਵ-ਸੂਚਕ ਮਿਲਿਆ', safe_detected: 'ਸੁਰੱਖਿਅਤ / ਘੱਟ-ਗੰਭੀਰ ਅਵਲੋਕਨ', violated_rule: 'ਉਲੰਘਿਆ ਨਿਯਮ', required_action: 'ਲੋੜੀਂਦੀ ਕਾਰਵਾਈ', stop_work: 'ਕੰਮ ਰੋਕੋ ਅਤੇ ਭੌਤਿਕ ਬੈਰੀਅਰ ਮੁੜ ਸਥਾਪਿਤ ਕਰੋ', field_scenarios: 'ਫੀਲਡ ਸੇਫਟੀ ਸਥਿਤੀਆਂ', safe_status: 'ਸੁਰੱਖਿਅਤ / ਨਿਯੰਤਰਿਤ', hse_dashboard: 'HSE ਸੇਫਟੀ ਡੈਸ਼ਬੋਰਡ', management_dashboard: 'ਪ੍ਰਬੰਧਨ ਡੈਸ਼ਬੋਰਡ', employee_dashboard: 'ਕਰਮਚਾਰੀ ਡੈਸ਼ਬੋਰਡ'
  },
  'தமிழ் (Tamil)': {
    title: 'OIL-SIF கட்டளை மையம்', subtitle: 'என்டர்பிரைஸ் SIF முன்னறிவிப்பு கண்டறிதல் மற்றும் பல்மொழி தடுப்பு நுண்ணறிவு இயந்திரம்', welcome: 'வரவேற்கிறோம்', logout: 'வெளியேறு / உள்நுழைவிற்கு திரும்பு', select_lang: 'இடைமுக மொழி', field_worker: 'கள பணியாளர்', hse_officer: 'HSE அதிகாரி', management: 'மேலாண்மை', command_modules: 'கட்டளை தொகுதிகள்', overview: 'மேலோட்டம்', report_analysis: 'அறிக்கை பகுப்பாய்வு', intelligence: 'நுண்ணறிவு', ai_copilot: 'AI கோ-பைலட்', my_dashboard: 'என் டாஷ்போர்டு', facility_node: 'வசதி முனை', engine_telemetry: 'எஞ்சின் டெலிமெட்ரி', authorized_operator: 'அங்கீகரிக்கப்பட்ட ஆபரேட்டர்', language: 'மொழி', role_protocol_active: 'புரோட்டோகோல் செயலில்', terminate_session: 'அமர்வை முடிக்கவும்', secure_credential_access: 'பாதுகாப்பான சான்று அணுகல்', credential_required: 'சான்றுகள் தேவை', role_based_access: 'பங்கு அடிப்படையிலான அணுகல்', authenticated_session: 'அங்கீகரிக்கப்பட்ட அமர்வு', sign_in: 'உள்நுழை', register_account: 'புதிய கணக்கை பதிவு செய்க', username: 'பயனர் பெயர்', password: 'கடவுச்சொல்', full_official_name: 'முழு அதிகாரப்பூர்வ பெயர்', new_username: 'புதிய பயனர் பெயர்', new_password: 'புதிய கடவுச்சொல்', designate_role: 'பங்கு நிலையைத் தேர்வு செய்க', authenticate_access: 'அணுகலை அங்கீகரிக்கவும்', register_user: 'பயனரை பதிவு செய்க', authenticating: 'அங்கீகரிக்கப்படுகிறது...', creating_account: 'கணக்கு உருவாக்கப்படுகிறது...', account_created: 'கணக்கு வெற்றிகரமாக உருவாக்கப்பட்டது. இப்போது பயனர் பெயர் மற்றும் கடவுச்சொல்லுடன் உள்நுழையலாம்.', demo_credentials: 'டெமோ சான்றுகள்', global_fleet_barrier: 'உலகளாவிய ஃப்ளீட் தடுப்பு சுகாதார டெலிமெட்ரி', login_required: 'தொடர உள்நுழையவும்.', invalid_credentials: 'பயனர் பெயர் அல்லது கடவுச்சொல் தவறாக உள்ளது.', all_fields_required: 'அனைத்து புலங்களும் அவசியம்.', loading: 'ஏற்றப்படுகிறது...', loading_intelligence: 'OIL-SIF நுண்ணறிவு ஏற்றப்படுகிறது...', unable_load_dashboard: 'டாஷ்போர்டு தரவை ஏற்ற முடியவில்லை.', total_reports: 'மொத்த அறிக்கைகள்', sif_potential: 'SIF சாத்தியம்', high_sif_probability: 'உயர் SIF சாத்தியம்', awaiting_hse_review: 'HSE மதிப்பாய்வு நிலுவையில்', reports_pending_validation: 'மனித சரிபார்ப்புக்காக நிலுவையில் உள்ள அறிக்கைகள்', sif_risk_overview: 'SIF ஆபத்து மேலோட்டம்', low_sif_probability: 'குறைந்த SIF சாத்தியம்', review_zone: 'மதிப்பாய்வு பகுதி', high_probability_band: 'உயர் SIF சாத்தியம்', top_recurring_precursors: 'முக்கிய மீண்டும் தோன்றும் முன்னறிவிப்புகள்', recent_high_risk: 'சமீபத்திய உயர்-ஆபத்து அறிக்கைகள்', safety_report_explorer: 'பாதுகாப்பு அறிக்கை எக்ஸ்ப்ளோரர்', search_placeholder: 'அறிக்கை ID, செயல்பாடு, முன்னறிவிப்பு அல்லது அறிக்கை உரையைத் தேடுங்கள்...', all: 'அனைத்தும்', pending_review: 'மதிப்பாய்வு நிலுவையில்', selected_safety_report: 'தேர்ந்தெடுக்கப்பட்ட பாதுகாப்பு அறிக்கை', run_ai_analysis: 'AI SIF பகுப்பாய்வை இயக்கவும்', analyzing_report: 'அறிக்கை பகுப்பாய்வு நடைபெறுகிறது...', ai_analysis_result: 'AI பகுப்பாய்வு முடிவு', precursor_intelligence: 'முன்னறிவிப்பு நுண்ணறிவு', barrier_analysis: 'தடை பகுப்பாய்வு', life_saving_rules: 'Life-Saving Rules', activity_risk: 'செயல்பாட்டு ஆபத்து', hse_review_queue: 'HSE மதிப்பாய்வு வரிசை', review: 'மதிப்பாய்வு', ai_safety_copilot: 'AI பாதுகாப்பு கோ-பைலட்', suggested_questions: 'பரிந்துரைக்கப்பட்ட கேள்விகள்', quick_queries: 'பொதுவான பாதுகாப்பு நுண்ணறிவு பணிகளுக்கான விரைவு கேள்விகள்', dataset_grounded_assistant: 'டேட்டாசெட் அடிப்படையிலான பாதுகாப்பு நுண்ணறிவு உதவியாளர்', analyzing_safety: 'பாதுகாப்பு நுண்ணறிவு பகுப்பாய்வு செய்யப்படுகிறது...', ask_copilot: 'OIL-SIF Copilot-ஐ கேளுங்கள்...', send: 'அனுப்பு →', hse_validation_notice: 'HSE சரிபார்ப்பு அறிவிப்பு', incident_hazard_scanner: 'நிகழ்வு மற்றும் அபாய முன்னறிவிப்பு ஸ்கேனர்', describe_hazard: 'கண்டறிந்த பாதுகாப்பற்ற நிலை அல்லது near miss-ஐ விளக்கவும்:', scan_btn: 'AI Guard மூலம் அபாயத்தை ஸ்கேன் செய்க', critical_detected: 'முக்கிய SIF முன்னறிவிப்பு கண்டறியப்பட்டது', safe_detected: 'பாதுகாப்பான / குறைந்த தீவிர கண்காணிப்பு', violated_rule: 'மீறப்பட்ட விதி', required_action: 'தேவையான நடவடிக்கை', stop_work: 'வேலையை நிறுத்தி உடல் தடுப்பை மீண்டும் நிறுவவும்', field_scenarios: 'கள பாதுகாப்பு சூழல்கள்', safe_status: 'பாதுகாப்பான / கட்டுப்படுத்தப்பட்ட', hse_dashboard: 'HSE பாதுகாப்பு டாஷ்போர்டு', management_dashboard: 'மேலாண்மை டாஷ்போர்டு', employee_dashboard: 'பணியாளர் டாஷ்போர்டு'
  },
  'తెలుగు (Telugu)': {
    title: 'OIL-SIF కమాండ్ హబ్', subtitle: 'ఎంటర్‌ప్రైజ్ SIF ముందస్తు సూచన గుర్తింపు మరియు బహుభాషా బ్యారియర్ ఇంటెలిజెన్స్ ఇంజిన్', welcome: 'స్వాగతం', logout: 'లాగ్ అవుట్ / లాగిన్‌కు తిరిగి వెళ్ళండి', select_lang: 'ఇంటర్‌ఫేస్ భాష', field_worker: 'ఫీల్డ్ ఉద్యోగి', hse_officer: 'HSE అధికారి', management: 'నిర్వహణ', command_modules: 'కమాండ్ మాడ్యూల్స్', overview: 'అవలోకనం', report_analysis: 'రిపోర్ట్ విశ్లేషణ', intelligence: 'ఇంటెలిజెన్స్', ai_copilot: 'AI కో-పైలట్', my_dashboard: 'నా డాష్‌బోర్డ్', facility_node: 'ఫెసిలిటీ నోడ్', engine_telemetry: 'ఇంజిన్ టెలిమెట్రీ', authorized_operator: 'అధీకృత ఆపరేటర్', language: 'భాష', role_protocol_active: 'ప్రోటోకాల్ సక్రియం', terminate_session: 'సెషన్ ముగించండి', secure_credential_access: 'సురక్షిత క్రెడెన్షియల్ యాక్సెస్', credential_required: 'క్రెడెన్షియల్స్ అవసరం', role_based_access: 'పాత్ర ఆధారిత యాక్సెస్', authenticated_session: 'ధృవీకరించబడిన సెషన్', sign_in: 'సైన్ ఇన్', register_account: 'కొత్త ఖాతా నమోదు', username: 'వినియోగదారు పేరు', password: 'పాస్‌వర్డ్', full_official_name: 'పూర్తి అధికారిక పేరు', new_username: 'కొత్త వినియోగదారు పేరు', new_password: 'కొత్త పాస్‌వర్డ్', designate_role: 'పాత్ర స్థాయిని ఎంచుకోండి', authenticate_access: 'యాక్సెస్ ధృవీకరించండి', register_user: 'వినియోగదారును నమోదు చేయండి', authenticating: 'ధృవీకరణ జరుగుతోంది...', creating_account: 'ఖాతా సృష్టిస్తోంది...', account_created: 'ఖాతా విజయవంతంగా సృష్టించబడింది. ఇప్పుడు వినియోగదారు పేరు మరియు పాస్‌వర్డ్‌తో సైన్ ఇన్ చేయండి.', demo_credentials: 'డెమో క్రెడెన్షియల్స్', global_fleet_barrier: 'గ్లోబల్ ఫ్లీట్ బ్యారియర్ హెల్త్ టెలిమెట్రీ', login_required: 'కొనసాగించడానికి సైన్ ఇన్ చేయండి.', invalid_credentials: 'వినియోగదారు పేరు లేదా పాస్‌వర్డ్ తప్పు.', all_fields_required: 'అన్ని ఫీల్డ్‌లు అవసరం.', loading: 'లోడ్ అవుతోంది...', loading_intelligence: 'OIL-SIF ఇంటెలిజెన్స్ లోడ్ అవుతోంది...', unable_load_dashboard: 'డాష్‌బోర్డ్ డేటా లోడ్ కాలేదు.', total_reports: 'మొత్తం రిపోర్టులు', sif_potential: 'SIF అవకాశం', high_sif_probability: 'అధిక SIF అవకాశం', awaiting_hse_review: 'HSE సమీక్ష పెండింగ్‌లో ఉంది', reports_pending_validation: 'మానవ ధృవీకరణ కోసం పెండింగ్‌లో ఉన్న రిపోర్టులు', sif_risk_overview: 'SIF ప్రమాద అవలోకనం', low_sif_probability: 'తక్కువ SIF అవకాశం', review_zone: 'సమీక్ష ప్రాంతం', high_probability_band: 'అధిక SIF అవకాశం', top_recurring_precursors: 'ప్రధానంగా పునరావృతమయ్యే ముందస్తు సూచనలు', recent_high_risk: 'ఇటీవలి అధిక-ప్రమాద రిపోర్టులు', safety_report_explorer: 'సేఫ్టీ రిపోర్ట్ ఎక్స్‌ప్లోరర్', search_placeholder: 'రిపోర్ట్ ID, కార్యకలాపం, ముందస్తు సూచన లేదా రిపోర్ట్ టెక్స్ట్ వెతకండి...', all: 'అన్నీ', pending_review: 'సమీక్ష పెండింగ్', selected_safety_report: 'ఎంచుకున్న సేఫ్టీ రిపోర్ట్', run_ai_analysis: 'AI SIF విశ్లేషణ నడపండి', analyzing_report: 'రిపోర్ట్ విశ్లేషణ జరుగుతోంది...', ai_analysis_result: 'AI విశ్లేషణ ఫలితం', precursor_intelligence: 'పూర్వసూచక ఇంటెలిజెన్స్', barrier_analysis: 'బ్యారియర్ విశ్లేషణ', life_saving_rules: 'Life-Saving Rules', activity_risk: 'కార్యకలాప ప్రమాదం', hse_review_queue: 'HSE సమీక్ష క్యూలో', review: 'సమీక్ష', ai_safety_copilot: 'AI సేఫ్టీ కో-పైలట్', suggested_questions: 'సూచించిన ప్రశ్నలు', quick_queries: 'సాధారణ సేఫ్టీ-ఇంటెలిజెన్స్ పనుల కోసం వేగవంతమైన ప్రశ్నలు', dataset_grounded_assistant: 'డేటాసెట్ ఆధారిత సేఫ్టీ ఇంటెలిజెన్స్ సహాయకుడు', analyzing_safety: 'సేఫ్టీ ఇంటెలిజెన్స్ విశ్లేషణ జరుగుతోంది...', ask_copilot: 'OIL-SIF Copilotని అడగండి...', send: 'పంపండి →', hse_validation_notice: 'HSE ధృవీకరణ నోటీసు', incident_hazard_scanner: 'ఘటన మరియు ప్రమాద పూర్వసూచక స్కానర్', describe_hazard: 'గమనించిన అసురక్షిత పరిస్థితి లేదా near miss వివరించండి:', scan_btn: 'AI Guardతో ప్రమాదాన్ని స్కాన్ చేయండి', critical_detected: 'తీవ్రమైన SIF పూర్వసూచకం గుర్తించబడింది', safe_detected: 'సురక్షితం / తక్కువ తీవ్రత గల పరిశీలన', violated_rule: 'ఉల్లంఘించిన నియమం', required_action: 'అవసరమైన చర్య', stop_work: 'పని నిలిపి భౌతిక బ్యారియర్‌ను పునరుద్ధరించండి', field_scenarios: 'ఫీల్డ్ సేఫ్టీ సందర్భాలు', safe_status: 'సురక్షితం / నియంత్రిత', hse_dashboard: 'HSE సేఫ్టీ డాష్‌బోర్డ్', management_dashboard: 'మేనేజ్‌మెంట్ డాష్‌బోర్డ్', employee_dashboard: 'ఉద్యోగి డాష్‌బోర్డ్'
  },
  'اردو (Urdu)': {
    title: 'OIL-SIF کمانڈ ہب', subtitle: 'انٹرپرائز SIF پیشگی اشاروں کی شناخت اور کثیر لسانی بیریئر انٹیلی جنس انجن', welcome: 'خوش آمدید', logout: 'لاگ آؤٹ / لاگ اِن پر واپس جائیں', select_lang: 'انٹرفیس زبان', field_worker: 'فیلڈ کارکن', hse_officer: 'HSE افسر', management: 'انتظامیہ', command_modules: 'کمانڈ ماڈیولز', overview: 'جائزہ', report_analysis: 'رپورٹ تجزیہ', intelligence: 'انٹیلی جنس', ai_copilot: 'AI کو پائلٹ', my_dashboard: 'میرا ڈیش بورڈ', facility_node: 'فیسلٹی نوڈ', engine_telemetry: 'انجن ٹیلی میٹری', authorized_operator: 'مجاز آپریٹر', language: 'زبان', role_protocol_active: 'پروٹوکول فعال', terminate_session: 'سیشن ختم کریں', secure_credential_access: 'محفوظ اسناد تک رسائی', credential_required: 'اسناد درکار ہیں', role_based_access: 'کردار پر مبنی رسائی', authenticated_session: 'مصدقہ سیشن', sign_in: 'سائن اِن', register_account: 'نیا اکاؤنٹ رجسٹر کریں', username: 'صارف نام', password: 'پاس ورڈ', full_official_name: 'پورا سرکاری نام', new_username: 'نیا صارف نام', new_password: 'نیا پاس ورڈ', designate_role: 'کردار کی سطح منتخب کریں', authenticate_access: 'رسائی کی تصدیق کریں', register_user: 'صارف رجسٹر کریں', authenticating: 'تصدیق جاری ہے...', creating_account: 'اکاؤنٹ بنایا جا رہا ہے...', account_created: 'اکاؤنٹ کامیابی سے بن گیا۔ اب صارف نام اور پاس ورڈ سے سائن اِن کریں۔', demo_credentials: 'ڈیمو اسناد', global_fleet_barrier: 'گلوبل فلیٹ بیریئر ہیلتھ ٹیلی میٹری', login_required: 'جاری رکھنے کے لیے سائن اِن کریں۔', invalid_credentials: 'صارف نام یا پاس ورڈ غلط ہے۔', all_fields_required: 'تمام خانے ضروری ہیں۔', loading: 'لوڈ ہو رہا ہے...', loading_intelligence: 'OIL-SIF انٹیلی جنس لوڈ ہو رہی ہے...', unable_load_dashboard: 'ڈیش بورڈ ڈیٹا لوڈ نہیں ہو سکا۔', total_reports: 'کل رپورٹس', sif_potential: 'SIF امکان', high_sif_probability: 'اعلی SIF امکان', awaiting_hse_review: 'HSE جائزہ زیر التوا', reports_pending_validation: 'انسانی توثیق کے منتظر رپورٹس', sif_risk_overview: 'SIF خطرے کا جائزہ', low_sif_probability: 'کم SIF امکان', review_zone: 'جائزہ علاقہ', high_probability_band: 'اعلی SIF امکان', top_recurring_precursors: 'بار بار آنے والے اہم پیشگی اشارے', recent_high_risk: 'حالیہ زیادہ خطرے والی رپورٹس', safety_report_explorer: 'حفاظتی رپورٹ ایکسپلورر', search_placeholder: 'رپورٹ ID، سرگرمی، پیشگی اشارہ یا رپورٹ متن تلاش کریں...', all: 'سب', pending_review: 'جائزہ زیر التوا', selected_safety_report: 'منتخب حفاظتی رپورٹ', run_ai_analysis: 'AI SIF تجزیہ چلائیں', analyzing_report: 'رپورٹ کا تجزیہ ہو رہا ہے...', ai_analysis_result: 'AI تجزیے کا نتیجہ', precursor_intelligence: 'پیشگی اشاروں کی انٹیلی جنس', barrier_analysis: 'بیریئر تجزیہ', life_saving_rules: 'Life-Saving Rules', activity_risk: 'سرگرمی کا خطرہ', hse_review_queue: 'HSE جائزہ قطار', review: 'جائزہ', ai_safety_copilot: 'AI حفاظتی کو پائلٹ', suggested_questions: 'تجویز کردہ سوالات', quick_queries: 'عام حفاظتی انٹیلی جنس کاموں کے لیے فوری سوالات', dataset_grounded_assistant: 'ڈیٹاسیٹ پر مبنی حفاظتی انٹیلی جنس معاون', analyzing_safety: 'حفاظتی انٹیلی جنس کا تجزیہ ہو رہا ہے...', ask_copilot: 'OIL-SIF Copilot سے پوچھیں...', send: 'بھیجیں →', hse_validation_notice: 'HSE توثیقی نوٹس', incident_hazard_scanner: 'واقعہ اور خطرے کے پیشگی اشارے اسکینر', describe_hazard: 'مشاہدہ شدہ غیر محفوظ حالت یا near miss بیان کریں:', scan_btn: 'AI Guard سے خطرہ اسکین کریں', critical_detected: 'سنگین SIF پیشگی اشارہ معلوم ہوا', safe_detected: 'محفوظ / کم شدت کا مشاہدہ', violated_rule: 'خلاف ورزی شدہ اصول', required_action: 'ضروری کارروائی', stop_work: 'کام روکیں اور جسمانی بیریئر دوبارہ قائم کریں', field_scenarios: 'فیلڈ حفاظتی حالات', safe_status: 'محفوظ / کنٹرول شدہ', hse_dashboard: 'HSE حفاظتی ڈیش بورڈ', management_dashboard: 'مینجمنٹ ڈیش بورڈ', employee_dashboard: 'ملازم ڈیش بورڈ'
  },
  'नेपाली (Nepali)': {
    title: 'OIL-SIF कमाण्ड हब', subtitle: 'इन्टरप्राइज SIF पूर्वसूचक पहिचान र बहुभाषिक ब्यारियर इन्टेलिजेन्स इन्जिन', welcome: 'स्वागत छ', logout: 'लग आउट / लगइनमा फर्कनुहोस्', select_lang: 'इन्टरफेस भाषा', field_worker: 'फिल्ड कर्मचारी', hse_officer: 'HSE अधिकृत', management: 'व्यवस्थापन', command_modules: 'कमाण्ड मोड्युल', overview: 'अवलोकन', report_analysis: 'रिपोर्ट विश्लेषण', intelligence: 'इन्टेलिजेन्स', ai_copilot: 'AI को-पाइलट', my_dashboard: 'मेरो ड्यासबोर्ड', facility_node: 'फ्यासिलिटी नोड', engine_telemetry: 'इन्जिन टेलिमेट्री', authorized_operator: 'अधिकृत अपरेटर', language: 'भाषा', role_protocol_active: 'प्रोटोकल सक्रिय', terminate_session: 'सत्र समाप्त गर्नुहोस्', secure_credential_access: 'सुरक्षित प्रमाणपत्र पहुँच', credential_required: 'प्रमाणपत्र आवश्यक', role_based_access: 'भूमिकामा आधारित पहुँच', authenticated_session: 'प्रमाणित सत्र', sign_in: 'साइन इन', register_account: 'नयाँ खाता दर्ता गर्नुहोस्', username: 'प्रयोगकर्ता नाम', password: 'पासवर्ड', full_official_name: 'पूरा आधिकारिक नाम', new_username: 'नयाँ प्रयोगकर्ता नाम', new_password: 'नयाँ पासवर्ड', designate_role: 'भूमिका स्तर छान्नुहोस्', authenticate_access: 'पहुँच प्रमाणित गर्नुहोस्', register_user: 'प्रयोगकर्ता दर्ता गर्नुहोस्', authenticating: 'प्रमाणीकरण हुँदैछ...', creating_account: 'खाता बनाउँदैछ...', account_created: 'खाता सफलतापूर्वक बन्यो। अब प्रयोगकर्ता नाम र पासवर्ड प्रयोग गरेर साइन इन गर्नुहोस्।', demo_credentials: 'डेमो प्रमाणपत्र', global_fleet_barrier: 'ग्लोबल फ्लीट ब्यारियर हेल्थ टेलिमेट्री', login_required: 'जारी राख्न साइन इन गर्नुहोस्।', invalid_credentials: 'प्रयोगकर्ता नाम वा पासवर्ड गलत छ।', all_fields_required: 'सबै फाँट आवश्यक छन्।', loading: 'लोड हुँदैछ...', loading_intelligence: 'OIL-SIF इन्टेलिजेन्स लोड हुँदैछ...', unable_load_dashboard: 'ड्यासबोर्ड डाटा लोड हुन सकेन।', total_reports: 'कुल रिपोर्ट', sif_potential: 'SIF सम्भावना', high_sif_probability: 'उच्च SIF सम्भावना', awaiting_hse_review: 'HSE समीक्षा पर्खाइमा', reports_pending_validation: 'मानव प्रमाणीकरण पर्खिरहेका रिपोर्टहरू', sif_risk_overview: 'SIF जोखिम अवलोकन', low_sif_probability: 'कम SIF सम्भावना', review_zone: 'समीक्षा क्षेत्र', high_probability_band: 'उच्च SIF सम्भावना', top_recurring_precursors: 'शीर्ष दोहोरिने पूर्वसूचक', recent_high_risk: 'हालैका उच्च-जोखिम रिपोर्टहरू', safety_report_explorer: 'सुरक्षा रिपोर्ट एक्सप्लोरर', search_placeholder: 'रिपोर्ट ID, गतिविधि, पूर्वसूचक वा रिपोर्ट पाठ खोज्नुहोस्...', all: 'सबै', pending_review: 'समीक्षा पर्खाइमा', selected_safety_report: 'छानिएको सुरक्षा रिपोर्ट', run_ai_analysis: 'AI SIF विश्लेषण चलाउनुहोस्', analyzing_report: 'रिपोर्ट विश्लेषण हुँदैछ...', ai_analysis_result: 'AI विश्लेषण परिणाम', precursor_intelligence: 'पूर्वसूचक इन्टेलिजेन्स', barrier_analysis: 'ब्यारियर विश्लेषण', life_saving_rules: 'Life-Saving Rules', activity_risk: 'गतिविधि जोखिम', hse_review_queue: 'HSE समीक्षा कतार', review: 'समीक्षा', ai_safety_copilot: 'AI सुरक्षा को-पाइलट', suggested_questions: 'सुझावित प्रश्नहरू', quick_queries: 'सामान्य सुरक्षा-इन्टेलिजेन्स कार्यका लागि द्रुत प्रश्नहरू', dataset_grounded_assistant: 'डाटासेटमा आधारित सुरक्षा इन्टेलिजेन्स सहायक', analyzing_safety: 'सुरक्षा इन्टेलिजेन्स विश्लेषण हुँदैछ...', ask_copilot: 'OIL-SIF Copilot लाई सोध्नुहोस्...', send: 'पठाउनुहोस् →', hse_validation_notice: 'HSE प्रमाणीकरण सूचना', incident_hazard_scanner: 'घटना र जोखिम पूर्वसूचक स्क्यानर', describe_hazard: 'देखिएको असुरक्षित अवस्था वा near miss को विवरण दिनुहोस्:', scan_btn: 'AI Guard बाट जोखिम स्क्यान गर्नुहोस्', critical_detected: 'गम्भीर SIF पूर्वसूचक फेला पर्यो', safe_detected: 'सुरक्षित / कम-गम्भीर अवलोकन', violated_rule: 'उल्लंघन गरिएको नियम', required_action: 'आवश्यक कार्य', stop_work: 'काम रोक्नुहोस् र भौतिक ब्यारियर पुनर्स्थापित गर्नुहोस्', field_scenarios: 'फिल्ड सुरक्षा अवस्था', safe_status: 'सुरक्षित / नियन्त्रित', hse_dashboard: 'HSE सुरक्षा ड्यासबोर्ड', management_dashboard: 'व्यवस्थापन ड्यासबोर्ड', employee_dashboard: 'कर्मचारी ड्यासबोर्ड'
  },
}

// Additional labels used by the current formal login/shell experience.
Object.assign(PACKS['हिन्दी (Hindi)'], {
  platform_name: 'सुरक्षा इंटेलिजेंस प्लेटफ़ॉर्म', login_headline: 'बेहतर संचालन के लिए', login_headline_2: 'सुरक्षा जानकारी।',
  login_intro: 'OIL-SIF सुरक्षा रिपोर्ट, गंभीर जोखिम स्क्रीनिंग, Life-Saving Rule मैपिंग और HSE समीक्षा को एक संरचित कार्यक्षेत्र में लाता है।',
  structured_workspace: 'संरचित कार्यक्षेत्र', structured_workspace_help: 'प्रत्येक उपयोगकर्ता की भूमिका के अनुसार स्पष्ट जानकारी व्यवस्थित की गई है।',
  role_based_access_help: 'अपनी जिम्मेदारियों से संबंधित उपकरण देखें।', hse_workflow: 'HSE workflow',
  hse_workflow_help: 'स्क्रीनिंग प्राथमिकता तय करने में सहायता करती है, जबकि अंतिम निर्णय योग्य HSE कर्मी लेते हैं।',
  secure_access: 'सुरक्षित एक्सेस', welcome_back: 'वापसी पर स्वागत है', sign_in_continue: 'अपने सुरक्षा कार्यक्षेत्र में जारी रखने के लिए साइन इन करें।',
  username_placeholder: 'अपना उपयोगकर्ता नाम दर्ज करें', password_placeholder: 'अपना पासवर्ड दर्ज करें', sign_in_securely: 'सुरक्षित रूप से साइन इन करें',
  sign_out_safely: 'सुरक्षित रूप से साइन आउट करें', system_operational: 'सिस्टम चालू है', dark_mode: 'डार्क मोड', light_mode: 'लाइट मोड',
  settings: 'सेटिंग्स', appearance: 'दिखावट', expanded: 'विस्तृत', collapsed: 'संक्षिप्त', close: 'बंद करें', notifications: 'सूचनाएँ',
  no_notifications: 'कोई नई सूचना नहीं।', help: 'सहायता', quick_help_title: 'OIL-SIF का उपयोग करने में सहायता चाहिए?', help_report: 'रिपोर्ट',
  help_report_text: 'असुरक्षित स्थिति या near miss का वर्णन आवाज़ या टाइप करके करें।', help_review: 'समीक्षा', help_review_text: 'क्या ध्यान देने की आवश्यकता है, यह देखने के लिए डैशबोर्ड का उपयोग करें।',
  help_assistant: 'सहायक से पूछें', help_assistant_text: 'सुरक्षा संबंधी प्रश्न सरल भाषा में पूछें।', read_aloud: 'जोर से पढ़ें', stop: 'रोकें',
  system_status: 'सिस्टम स्थिति', status_note: 'स्थिति जाँच इस सत्र में उपलब्ध एप्लिकेशन सेवाओं को दर्शाती है।', workspace: 'कार्यक्षेत्र', main_navigation: 'मुख्य नेविगेशन',
  need_help: 'सहायता चाहिए?', sidebar_help: 'सरल भाषा में मार्गदर्शन के लिए Safety Assistant का उपयोग करें।', open_help: 'सहायता खोलें'
})

// Generic fallback packs for the remaining scheduled languages. The key UI
// labels are localized, while safety standards/acronyms remain bilingual.

PACKS.English = { ...PACKS.English, voice_transcription: 'Voice transcription', stop_voice: 'Stop voice', listening: 'Listening… speak clearly', voice_help: 'Speak your observation and it will be converted to text.', voice_unsupported: 'Voice transcription is not supported in this browser. Please use Google Chrome or Microsoft Edge.', voice_permission: 'Microphone permission was denied. Please allow microphone access and try again.', voice_error: 'Voice transcription could not be completed. Please try again.', site_safety_snapshot: 'Site Safety Snapshot', common_hazards: 'Common hazards', top_lsr: 'Top Life-Saving Rule', recent_alerts: 'Recent safety alerts', recurring_site_pattern: 'Recurring safety pattern to watch', follow_rule: 'Follow the applicable Life-Saving Rule before starting work', high_risk_alerts: 'High-risk observations available for awareness', no_hazard_data: 'No hazard data', recommended_precautions: 'Recommended precautions', employee_precautions_help: 'Simple controls to check before and during work.', precaution_barrier: 'Verify the physical barrier before work starts.', precaution_lsr: 'Confirm the applicable Life-Saving Rule.', precaution_stop: 'Stop if a critical precursor appears.', precaution_report: 'Report unsafe conditions and near misses promptly.', general_alerts_only: 'General safety information — no individual employee details.', safety_alert: 'Safety alert', no_alerts: 'No recent alerts to display.', top_life_saving_rules: 'Top Life-Saving Rules', employee_lsr_help: 'Use these as a quick field reminder.' }

const LATIN_LIKE = {
  'कोंकणी (Konkani)': 'कोंकणी',
  'बोडो (Bodo)': 'बोडो',
  'डोगरी (Dogri)': 'डोगरी',
  'मैथिली (Maithili)': 'मैथिली',
  'मৈতৈলোন (Meitei / Manipuri)': 'মৈতৈলোন',
  'संस्कृत (Sanskrit)': 'संस्कृत',
  'سنڌي (Sindhi)': 'سنڌي',
  'کٲشُر (Kashmiri)': 'کٲشُر',
}

for (const language of Object.keys(LATIN_LIKE)) {
  const label = LATIN_LIKE[language]
  PACKS[language] = {
    title: `OIL-SIF ${label} कमांड हब`,
    subtitle: `SIF पूर्वसूचक पहिचान तथा बहुभाषिक सुरक्षा ब्यारियर इंटेलिजेंस प्रणाली`,
    welcome: language.includes('سنڌي') ? 'ڀليڪار' : 'स्वागतम्',
    logout: language.includes('سنڌي') ? 'لاگ آئوٽ / واپس لاگ اِن' : 'लॉग आउट / लॉगिन पर वापस जाएँ',
    select_lang: 'इंटरफ़ेस भाषा',
    field_worker: 'फील्ड कर्मचारी',
    hse_officer: 'HSE अधिकारी',
    management: 'प्रबंधन',
    command_modules: 'कमांड मॉड्यूल',
    overview: 'अवलोकन',
    report_analysis: 'रिपोर्ट विश्लेषण',
    intelligence: 'इंटेलिजेंस',
    ai_copilot: 'AI सह-पायलट',
    my_dashboard: 'मेरा डैशबोर्ड',
    facility_node: 'फैसिलिटी नोड',
    engine_telemetry: 'इंजन टेलीमेट्री',
    authorized_operator: 'अधिकृत ऑपरेटर',
    language: 'भाषा',
    role_protocol_active: 'प्रोटोकॉल सक्रिय',
    terminate_session: 'सत्र समाप्त करें',
    secure_credential_access: 'सुरक्षित क्रेडेंशियल एक्सेस',
    credential_required: 'क्रेडेंशियल आवश्यक',
    role_based_access: 'भूमिका-आधारित एक्सेस',
    authenticated_session: 'प्रमाणित सत्र',
    sign_in: 'साइन इन',
    register_account: 'नया खाता पंजीकृत करें',
    username: 'उपयोगकर्ता नाम',
    password: 'पासवर्ड',
    full_official_name: 'पूरा आधिकारिक नाम',
    new_username: 'नया उपयोगकर्ता नाम',
    new_password: 'नया पासवर्ड',
    designate_role: 'भूमिका स्तर चुनें',
    authenticate_access: 'एक्सेस प्रमाणित करें',
    register_user: 'उपयोगकर्ता पंजीकृत करें',
    authenticating: 'प्रमाणीकरण हो रहा है...',
    creating_account: 'खाता बनाया जा रहा है...',
    account_created: 'खाता सफलतापूर्वक बनाया गया। अब आप उपयोगकर्ता नाम और पासवर्ड से साइन इन कर सकते हैं।',
    demo_credentials: 'डेमो क्रेडेंशियल',
    global_fleet_barrier: 'ग्लोबल फ्लीट बैरियर हेल्थ टेलीमेट्री',
    login_required: 'जारी रखने के लिए कृपया साइन इन करें।',
    invalid_credentials: 'उपयोगकर्ता नाम या पासवर्ड गलत है।',
    all_fields_required: 'सभी फ़ील्ड आवश्यक हैं।',
    loading: 'लोड हो रहा है...',
    loading_intelligence: 'OIL-SIF इंटेलिजेंस लोड हो रही है...',
    unable_load_dashboard: 'डैशबोर्ड डेटा लोड नहीं हो सका।',
    total_reports: 'कुल रिपोर्ट',
    sif_potential: 'SIF संभावित',
    high_sif_probability: 'उच्च SIF संभावना',
    awaiting_hse_review: 'HSE समीक्षा लंबित',
    reports_pending_validation: 'मानवीय सत्यापन की प्रतीक्षा में रिपोर्ट',
    sif_risk_overview: 'SIF जोखिम अवलोकन',
    low_sif_probability: 'कम SIF संभावना',
    review_zone: 'समीक्षा क्षेत्र',
    high_probability_band: 'उच्च SIF संभावना',
    top_recurring_precursors: 'शीर्ष बार-बार आने वाले पूर्वसूचक',
    recent_high_risk: 'हाल की उच्च-जोखिम रिपोर्ट',
    safety_report_explorer: 'सुरक्षा रिपोर्ट एक्सप्लोरर',
    search_placeholder: 'रिपोर्ट ID, गतिविधि, पूर्वसूचक या रिपोर्ट टेक्स्ट खोजें...',
    all: 'सभी',
    pending_review: 'समीक्षा लंबित',
    selected_safety_report: 'चयनित सुरक्षा रिपोर्ट',
    run_ai_analysis: 'AI SIF विश्लेषण चलाएँ',
    analyzing_report: 'रिपोर्ट का विश्लेषण हो रहा है...',
    ai_analysis_result: 'AI विश्लेषण परिणाम',
    precursor_intelligence: 'पूर्वसूचक इंटेलिजेंस',
    barrier_analysis: 'बैरियर विश्लेषण',
    life_saving_rules: 'Life-Saving Rules',
    activity_risk: 'गतिविधि जोखिम',
    hse_review_queue: 'HSE समीक्षा कतार',
    review: 'समीक्षा',
    ai_safety_copilot: 'AI सुरक्षा सह-पायलट',
    suggested_questions: 'सुझाए गए प्रश्न',
    quick_queries: 'सामान्य सुरक्षा-इंटेलिजेंस कार्यों के लिए त्वरित प्रश्न',
    dataset_grounded_assistant: 'डेटासेट-आधारित सुरक्षा इंटेलिजेंस सहायक',
    analyzing_safety: 'सुरक्षा इंटेलिजेंस का विश्लेषण हो रहा है...',
    ask_copilot: 'OIL-SIF Copilot से पूछें...',
    send: 'भेजें →',
    hse_validation_notice: 'HSE सत्यापन सूचना',
    incident_hazard_scanner: 'घटना एवं खतरा पूर्वसूचक स्कैनर',
    describe_hazard: 'देखी गई असुरक्षित स्थिति या near miss का विवरण दें:',
    scan_btn: 'AI Guard से खतरा स्कैन करें',
    critical_detected: 'गंभीर SIF पूर्वसूचक पाया गया',
    safe_detected: 'सुरक्षित / कम-गंभीर अवलोकन',
    violated_rule: 'उल्लंघन किया गया नियम',
    required_action: 'आवश्यक कार्रवाई',
    stop_work: 'काम रोकें और भौतिक बैरियर पुनः स्थापित करें',
    field_scenarios: 'फील्ड सुरक्षा परिदृश्य',
    safe_status: 'सुरक्षित / नियंत्रित',
    hse_dashboard: 'HSE सुरक्षा डैशबोर्ड',
    management_dashboard: 'प्रबंधन डैशबोर्ड',
    employee_dashboard: 'कर्मचारी डैशबोर्ड',
  }
}

export const TRANSLATIONS = {
  English: { ...EN },
  ...Object.fromEntries(
    LANGUAGES.filter((language) => language !== 'English').map((language) => [
      language,
      { ...EN, ...(PACKS[language] || {}) },
    ])
  ),
}


// Language is rendered through React state. Do not mutate DOM text nodes here;
// doing so causes translated text to become the next language's source text.
export { installLanguageObserver } from './translations_runtime.js'
export function applyLanguageToDocument() {}
