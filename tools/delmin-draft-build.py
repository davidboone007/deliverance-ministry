# Builds the delmin.org revamp draft into the Lambs to Lions site repo (lambs2lions.org) at /delmin.org-draft/.
# Edit the page bodies here, then run from the repo root: python3 tools/delmin-draft-build.py
# and again with --combined for the version styled after Lambs to Lions.
import hashlib, re, pathlib, sys, html as H
# --combined builds the version that blends in the Lambs to Lions look, into delmin.org-draft/combined/
COMBINED = True   # only the combined style is kept (David, 2026-11-26)
args = [x for x in sys.argv[1:] if not x.startswith("--")]
ROOT = pathlib.Path(__file__).resolve().parent.parent / "delmin.org-draft"
OUT = pathlib.Path(args[0]) if args else ROOT
OUT.mkdir(parents=True, exist_ok=True)
IMG = ""
SITE = "Deliverance Ministries"
OLD = "https://delmin.org"          # old WordPress site (down since 2026-11-09)
UP = IMG + "media/"                # testimony MP3s and handout PDFs, recovered from the Internet Archive

LOGO = '''<svg viewBox="0 0 40 40" aria-hidden="true"><circle cx="20" cy="20" r="19" fill="#c08a2b"/><path d="M20 7v26M12 15h16" stroke="#fff" stroke-width="3.4" stroke-linecap="round"/><path d="M8.5 28.5c3-2.2 5.2-2.2 7 0M24.5 28.5c1.8-2.2 4-2.2 7 0" stroke="#17394a" stroke-width="2" fill="none" stroke-linecap="round"/></svg>'''

def tbc(t="to confirm"):
    return f'<span class="tbc" title="Draft: fact still to confirm">{t}</span>'

def page(fname, title, desc, body, current):
    links = [("get-help.html","Get help"),("learn.html","Learn to minister"),("churches.html","For churches"),("testimonies.html","Testimonies"),("give.html","Give")]
    def a(h,t):
        cur = ' aria-current="page"' if h==current else ''
        cls = ' class="cta"' if h=="give.html" else ''
        return f'<a href="{h}"{cur}{cls}>{t}</a>'
    nav = "".join(a(h,t) for h,t in links)
    doc = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" href="brand/favicon-32.png" type="image/png">
<link rel="apple-touch-icon" href="brand/apple-touch-icon.png">
<link rel="stylesheet" href="style.css?v={hashlib.sha1(CSS.encode()).hexdigest()[:8]}">
</head>
<body>
<div class="draftbar">Draft preview of a new delmin.org. Not the live site yet. Forms work, and <span class="tbc">highlighted</span> facts are still being confirmed.</div>
<header class="top"><div class="wrap">
<a class="brand" href="index.html">{LOGO}<span>{SITE}</span></a>
<nav>{nav}</nav>
</div></header>
<main>
{body}
</main>
<footer><div class="wrap">
<div class="fgrid">
<div><p><b>{SITE} Inc</b><br>Oklahoma City, Oklahoma<br>Serving since 1984</p>
<p>All ministry is free of charge. “Freely you received, so freely give.” <span class="ref">Matthew 10:8</span></p></div>
<div><p><a href="about.html">About the ministry</a><br><a href="contact.html">Contact us</a><br><a href="get-help.html">Get help</a><br><a href="give.html">Give</a></p></div>
<div><p>Phone (405) 842-5509<br><a href="mailto:delmin.org@gmail.com">delmin.org@gmail.com</a><br>Mail: 2828 NW 57th, Ste. 305<br>Oklahoma City, OK 73112</p></div>
</div>
<p class="small">Scripture quotations are from the World English Bible (public domain), except where noted.</p>
</div></footer>
</body>
</html>
'''
    (OUT/fname).write_text(doc)

# Forms post to Web3Forms, which emails each submission. The access key decides the inbox.
# TEMPORARY: this is David's Lambs to Lions (lambs2lions.org) key, so messages reach David until a key is
# made for delmin.org@gmail.com at web3forms.com (then replace FORM_KEY).
FORM_KEY = "d9fb3c2a-e827-4b5b-87e1-b6060e60867f"
SITE_URL = "https://lambs2lions.org/delmin.org-draft/"
# Form inbox (Google Sheet + Apps Script owned by delmin.org@gmail.com, set up 2026-11-26). Each submission
# becomes a row in the sheet and the script emails delmin.org@gmail.com. If that post fails, the form falls
# back to Web3Forms (action= below) so the message still arrives by email.
SHEET_URL = "https://script.google.com/macros/s/AKfycbzOfph8SqL-3Y9Pk4ugDQLFWClMbWK76fbW9MI5Yf4Pdo9GuWHadG49qELy9HiuW9tc/exec"

def form(title, fields, button="Send request"):
    def named(m):
        label = H.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip()
        req = " required" if label in ("Your name", "Email") else ""
        nm = {"Your name": "name", "Email": "email"}.get(label, label)  # Web3Forms uses "email" as the reply-to
        return f'<label>{m.group(1)}</label><{m.group(2)} name="{H.escape(nm)}"{req}'
    fields = re.sub(r'<label>(.*?)</label><(input|select|textarea)', named, fields)
    return f'''<form class="card form" action="https://api.web3forms.com/submit" method="POST" onsubmit="event.preventDefault();var f=this,n=f.elements.name.value||'someone',b=f.querySelector('button');f.elements.subject.value='delmin.org: {H.escape(title.replace(chr(39), chr(92)+chr(39)))} from '+n+' ('+new Date().toLocaleString()+')';b.disabled=true;b.textContent='Sending…';fetch('{SHEET_URL}',{{method:'POST',mode:'no-cors',body:new URLSearchParams(new FormData(f))}}).then(function(){{location.href=f.elements.redirect.value}}).catch(function(){{f.submit()}});">
<input type="hidden" name="access_key" value="{FORM_KEY}">
<input type="hidden" name="subject" value="delmin.org: {H.escape(title)}">
<input type="hidden" name="from_name" value="delmin.org website">
<input type="hidden" name="Form" value="{H.escape(title)}">
<input type="hidden" name="redirect" value="{SITE_URL}thanks.html">
<input type="checkbox" name="botcheck" style="display:none" tabindex="-1" autocomplete="off">
<h3>{title}</h3>
{fields}
<div><button class="btn" type="submit">{button}</button></div>
</form>'''

LANG = '<div class="row2"><div><label>Language for ministry</label><select><option>English</option><option>Spanish</option><option>Other (please say which)</option></select></div><div><label>Other language (optional)</label><input type="text"></div></div><p class="small muted">Our ministers mainly speak English. Another language depends on whether a minister who speaks it is available.</p>'

COUNTRIES = ['United States', 'Afghanistan', 'Albania', 'Algeria', 'American Samoa', 'Andorra', 'Angola', 'Anguilla', 'Antarctica', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Aruba', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bermuda', 'Bhutan', 'Bolivia', 'Bonaire, Sint Eustatius and Saba', 'Bosnia and Herzegovina', 'Botswana', 'Bouvet Island', 'Brazil', 'British Indian Ocean Territory', 'Brunei', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cabo Verde', 'Cambodia', 'Cameroon', 'Canada', 'Cayman Islands', 'Central African Republic', 'Chad', 'Chile', 'China', 'Christmas Island', 'Cocos (Keeling) Islands', 'Colombia', 'Comoros', 'Congo (DRC)', 'Congo (Republic)', 'Cook Islands', 'Costa Rica', 'Croatia', 'Cuba', 'Curaçao', 'Cyprus', 'Czech Republic', "Côte d'Ivoire", 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Eswatini', 'Ethiopia', 'Falkland Islands (Malvinas)', 'Faroe Islands', 'Fiji', 'Finland', 'France', 'French Guiana', 'French Polynesia', 'French Southern Territories', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Gibraltar', 'Greece', 'Greenland', 'Grenada', 'Guadeloupe', 'Guam', 'Guatemala', 'Guernsey', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Heard Island and McDonald Islands', 'Honduras', 'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Isle of Man', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jersey', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macao', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Martinique', 'Mauritania', 'Mauritius', 'Mayotte', 'Mexico', 'Micronesia', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro', 'Montserrat', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New Caledonia', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Niue', 'Norfolk Island', 'North Korea', 'North Macedonia', 'Northern Mariana Islands', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestine', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Pitcairn', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 'Romania', 'Russia', 'Rwanda', 'Réunion', 'Saint Barthélemy', 'Saint Helena, Ascension and Tristan da Cunha', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Martin (French part)', 'Saint Pierre and Miquelon', 'Saint Vincent and the Grenadines', 'Samoa', 'San Marino', 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Sint Maarten (Dutch part)', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'South Georgia and the South Sandwich Islands', 'South Korea', 'South Sudan', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'Svalbard and Jan Mayen', 'Sweden', 'Switzerland', 'Syria', 'Taiwan', 'Tajikistan', 'Tanzania', 'Thailand', 'Timor-Leste', 'Togo', 'Tokelau', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Turks and Caicos Islands', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States Minor Outlying Islands', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Vatican City', 'Venezuela', 'Vietnam', 'Virgin Islands, British', 'Virgin Islands, U.S.', 'Wallis and Futuna', 'Western Sahara', 'Yemen', 'Zambia', 'Zimbabwe', 'Åland Islands']  # United States first, then A-Z (from ISO 3166, 2026-11-26)
NAME_EMAIL = '''<div class="row2">
<div><label>Your name</label><input type="text" autocomplete="name"></div>
<div><label>Email</label><input type="email" autocomplete="email"></div>
</div>
<div class="row2">
<div><label>Phone</label><input type="tel" autocomplete="tel" placeholder="Include country code if outside the US"></div>
<div><label>Country</label><select autocomplete="country-name">''' + ''.join(f'<option>{H.escape(c)}</option>' for c in COUNTRIES) + '''</select></div>
</div>
<div class="row2">
<div><label>City</label><input type="text" autocomplete="address-level2"></div>
<div><label>State / province / region</label><input type="text" autocomplete="address-level1"></div>
</div>'''

def yt(vid, title, length=""):
    meta = f'<span class="len">{length}</span>' if length else ''
    return f'''<figure class="video"><div class="frame"><iframe loading="lazy" src="https://www.youtube-nocookie.com/embed/{vid}" title="{H.escape(title)}" allow="encrypted-media; picture-in-picture" allowfullscreen></iframe></div><figcaption>{title} {meta}</figcaption></figure>'''

ICON = {
 "near": '<svg viewBox="0 0 48 48"><path d="M24 44s14-13 14-24a14 14 0 0 0-28 0c0 11 14 24 14 24z" fill="#5f0423"/><circle cx="24" cy="20" r="5.5" fill="#fff"/></svg>',
 "far": '<svg viewBox="0 0 48 48"><rect x="13" y="5" width="22" height="38" rx="4" fill="#5f0423"/><rect x="16" y="10" width="16" height="25" rx="1.5" fill="#fff"/><circle cx="24" cy="39" r="1.8" fill="#fff"/><path d="M20 19l4 3-4 3z" fill="#00622c"/></svg>',
 "child": '<svg viewBox="0 0 48 48"><circle cx="17" cy="11" r="6" fill="#5f0423"/><path d="M7 44V27a10 10 0 0 1 20 0v17z" fill="#5f0423"/><circle cx="34" cy="21" r="4.5" fill="#00622c"/><path d="M27 44V33a7 7 0 0 1 14 0v11z" fill="#00622c"/></svg>',
 "learn": '<svg viewBox="0 0 48 48"><path d="M6 10c7-2 13-1 18 3 5-4 11-5 18-3v28c-7-2-13-1-18 3-5-4-11-5-18-3z" fill="#5f0423"/><path d="M24 13v28" stroke="#fff" stroke-width="2"/></svg>',
 "church": '<svg viewBox="0 0 48 48"><path d="M24 4v10M20 8h8" stroke="#5f0423" stroke-width="3" stroke-linecap="round"/><path d="M10 44V26l14-11 14 11v18z" fill="#5f0423"/><path d="M20 44v-9a4 4 0 0 1 8 0v9z" fill="#00622c"/></svg>',
 "give": '<svg viewBox="0 0 48 48"><path d="M24 42S6 31 6 18a9 9 0 0 1 18-3 9 9 0 0 1 18 3c0 13-18 24-18 24z" fill="#00622c"/></svg>',
}

def persona(icon, href, title, text, go):
    return f'<a class="persona" href="{href}">{ICON[icon]}<h3>{title}</h3><p>{text}</p><span class="go">{go} →</span></a>'

PERSONAS = "".join([
 persona("near","help-nearby.html","I'd like ministry in person","Come to a Monday night meeting in Oklahoma City for free, one-on-one ministry. Whether you live nearby or travel to come, you're welcome.","Monday nights"),
 persona("far","help-anywhere.html","I need help, but can't come in person","Start a step-by-step guide at home, then meet a minister by phone, Zoom or FaceTime.","Help from anywhere"),
 persona("child","children.html","I'm a parent seeking help for my child","How ministry for children works, and how to request an appointment.","Help for children"),
 persona("learn","learn.html","I want to learn to minister","Free training videos, handouts and a place on the Monday team.","Training"),
 persona("church","churches.html","I lead a church or group","Invite a team to teach, minister and train your people.","Invite us"),
 persona("give","give.html","I want to support this ministry","Every session is free. Gifts keep it that way.","Ways to give"),
])

# ---------------- HOME ----------------
HOME = f'''
<section class="hero"><div class="wrap">
<h1>Freedom and healing in Jesus Christ</h1>
<p class="lead">Depression, fear, addiction, illness, guilt, heartache or trauma don't have to have the last word. Jesus still sets people free today, and every ministry session here is free of charge.</p>
<blockquote>“If therefore the Son makes you free, you will be free indeed.” <span class="ref">John 8:36</span></blockquote>
<a class="btn" href="#help">Find the help that fits you</a>
</div></section>

<section id="help"><div class="wrap">
<h2 class="center">How can we help you?</h2>
<div class="personas">{PERSONAS}</div>
</div></section>

<section class="band"><div class="wrap two">
<div>
<h2>Monday nights in Oklahoma City</h2>
<ol class="timeline">
<li><b>5:30 pm</b> Introduction and teaching</li>
<li><b>6:30 pm</b> Door-closing prayer, together <span class="pill">required</span></li>
<li><b>7:30 pm</b> Personal ministry, ending by 10:30 pm at the latest</li>
</ol>
<p>9201 N. Rockwell, Oklahoma City, OK 73132<br><span class="muted">West side of Rockwell, between NW Expressway and Britton Rd.</span></p>
<p>Everyone is welcome, whether you live nearby or travel to come.</p>
<a class="btn" href="help-nearby.html">Plan your visit</a>
</div>
<div class="card quote">
<p>“The Spirit of the Lord is on me, because he has anointed me to preach good news to the poor. He has sent me to heal the broken hearted, to proclaim release to the captives, recovering of sight to the blind, to deliver those who are crushed.”</p>
<p class="ref">Luke 4:18</p>
</div>
</div></section>

<section><div class="wrap two">
<div>
<h2>Hear what God has done</h2>
<p>Nearly thirty people share, in their own voices, how Jesus healed their bodies, broke addictions, restored marriages and freed them from fear.</p>
<a class="btn ghost" href="testimonies.html">Listen to testimonies</a>
</div>
<div>
<h2>Always free</h2>
<p>We never charge for ministry. Our trained ministers serve as volunteers, and the work is carried by the gifts of people who have been set free.</p>
<a class="btn ghost" href="give.html">Support the ministry</a>
</div>
</div></section>
'''

# ---------------- GET HELP (hub) ----------------
GETHELP = f'''
<section class="page-hero"><div class="wrap">
<h1>Get help</h1>
<p>Ministry is free, personal and confidential. Choose the path that fits you.</p>
</div></section>
<section><div class="wrap">
<div class="personas three">
{persona("near","help-nearby.html","In person","Come to a Monday night meeting in Oklahoma City. Visitors from out of town are welcome.","Monday nights")}
{persona("far","help-anywhere.html","From anywhere","A guide at home, then phone, Zoom or FaceTime.","Help from anywhere")}
{persona("child","children.html","For your child","Parents first, then an appointment.","Help for children")}
</div>
<div class="card soft">
<h3>What happens in ministry</h3>
<ol class="steps">
<li><b>Learn.</b> What Jesus did and still does, how evil spirits gain a foothold, and the authority believers have in His name.</li>
<li><b>Close the doors.</b> Forgive, repent and renounce in a door-closing prayer, cancelling any legal right evil spirits have claimed.</li>
<li><b>Break ungodly soul ties</b> and receive <b>inner healing</b> for past wounds.</li>
<li><b>Deliverance.</b> Evil spirits are commanded to leave in Jesus' name.</li>
<li><b>Healing.</b> We pray for physical healing and for the fullness of the Holy Spirit.</li>
<li><b>Stay free.</b> You leave with simple practices to walk in freedom.</li>
</ol>
</div>
</div></section>
'''

# ---------------- NEARBY ----------------
NEARBY = f'''
<section class="page-hero"><div class="wrap">
<h1>Monday nights in Oklahoma City</h1>
<p>Free, one-on-one ministry with trained ministers, every Monday except major holidays. Whether you live nearby or are willing to travel, you are welcome.</p>
</div></section>
<section><div class="wrap two">
<div>
<h2>Your evening</h2>
<ol class="timeline">
<li><b>5:30 pm</b> Introduction: Jesus' works today, how evil spirits gain access, your authority in Christ, and staying free.</li>
<li><b>6:30 pm</b> Door-closing prayer together. <span class="pill">required before personal ministry</span></li>
<li><b>7:30 pm</b> Personal ministry with a small team. Sessions end by 10:30 pm at the latest.</li>
</ol>
<h2>Before you come</h2>
<ul class="check">
<li>Print the <a href="{UP}problem-list.pdf">Problem List</a> and circle anything that applies to you.</li>
<li>Reserve your Monday with the form on this page.</li>
<li>Plan to stay the whole evening.</li>
<li>No childcare is available. See <a href="children.html">help for children</a>.</li>
</ul>
<h2>Where</h2>
<p>9201 N. Rockwell, Oklahoma City, OK 73132<br><span class="muted">West side of Rockwell, between NW Expressway and Britton Rd.</span><br><a href="https://maps.google.com/?q=9201+N+Rockwell+Ave,+Oklahoma+City,+OK+73132">Open in Maps</a></p>
</div>
<div>
{form("Reserve a Monday", NAME_EMAIL + LANG + '<div><label>Which Monday?</label><select id="monday-pick"><option>Next available Monday</option></select></div><script>(function(){var s=document.getElementById(\'monday-pick\'),d=new Date();d.setHours(0,0,0,0);d.setDate(d.getDate()+((8-d.getDay())%7));for(var i=0;i<12;i++){var o=document.createElement(\'option\');o.textContent=d.toLocaleDateString(\'en-US\',{weekday:\'long\',month:\'long\',day:\'numeric\',year:\'numeric\'});s.appendChild(o);d.setDate(d.getDate()+7)}})();</script><div><label>Anything we should know? (optional)</label><textarea></textarea></div>', "Reserve")}
<div class="card soft"><h3>Topics we often see</h3><p class="muted">Including but not limited to:</p>
<p>fear and anxiety · depression · addictions · eating disorders · sickness and infirmity · witchcraft and the occult · multiple personalities · troubled homes · emotional wounds</p></div>
</div>
</div></section>
'''

# ---------------- ANYWHERE ----------------
PROBLEMS = [('Bitterness', ['Hate', 'Self-Hate', 'Offense', 'Regret', 'Unforgiveness', 'Unforgiveness of self', 'Hurt', 'Unjustness', 'Injustice', 'Resentment', 'Murder', 'Revenge', 'Retaliation', 'Jealousy', 'Envy', 'Anger at God', 'Blaming God'], None), ('Rejection', ['Fear of Rejection', 'Self-Rejection', 'Rejection in the Womb'], None), ('Rebellion', ['Self-Will', 'Stubbornness', 'Disobedience', 'Anti-Submissiveness', 'False Prophet Spirit'], None), ('Destroyer', ['Withdrawal', 'Separation of Relationships', 'Separation of Marriages', 'Compromise', 'Division', 'Divorce', 'Self-Destruction', 'Self-Mutilation', 'Failure', 'Tragedy', 'Sabotage'], None), ('Death', ['Death Wish', 'Death of Dreams', 'Suicide', 'Murder', 'Abortion', 'By Infirmity', 'By Accident', 'Driving too fast'], None), ('Deception (accepting lies)', ['Self-Deception', 'Delusion', 'Blinding', 'Deceit', 'Denial', 'Memory Recall', 'Lies to the mind'], None), ('Anger', ['Rage', 'Wrath', 'Temper', 'Irrational Anger', 'Self-Anger', 'Violence'], None), ('Deaf & Mute', ['Seizures', 'Convulsions', 'Deafness (physical)', 'Deafness (spiritual)'], None), ('Control', ['“Gatekeeper”', 'Ruler', 'Manipulation', 'Chauvinism', 'Misogyny', 'Possessiveness', 'Domineering'], None), ('Condemnation', ['Guilt', 'Embarrassment', 'Unworthiness', 'Frustration', 'Defeatism', 'Discouragement', 'Accusations', 'Inferiority', 'Insecurity', 'Shame', 'Death Wish', 'Shyness', 'Timidity', 'Intimidation', 'Oversensitive'], None), ('Confusion', ['Forgetfulness', 'Mind Control', 'Mind Blocking', 'Mind Hindering', 'Soul Fragmenting (feeling broken inside)', 'Indifference', 'Double-Mindedness', 'Procrastination', 'Illiteracy'], None), ('Cravings & Addictions', ['Alcohol', 'Nicotine', 'Drugs', 'Medications', 'Gluttony', 'Food', 'Sweets', 'Overeating', 'Fear of Starvation', 'Caffeine', 'Affection', 'Sex', 'Pornography', 'Gambling', 'Vaping', 'Cannabis', 'Pain Pills', 'Opioids', 'Shopping', 'Spending', 'Craving of Things', 'Video Games', 'Social Media', 'Cell Phone Screen Time', 'Idolatry of the above'], None), ('Bondage', ['Hyperactivity (ADHD)', 'Overbearing', 'Talkative', 'Impatience', 'Stealing (Kleptomania)', 'Cheating', 'Physical Pain', 'Victim', 'Blocked Emotion', 'Affection', 'Blocked Completion', 'Frigidity', 'Feeling Cold or Hot for No Reason', 'Workaholic', 'Perfectionism', 'Trauma', 'Birth Trauma', 'Tension Headache', 'Migraine', 'Insomnia', 'Escapism', 'Racism', 'Compulsions', 'Competition', 'Stingy', 'Hoarding', 'Unclean', 'Messiness', 'Bulimia', 'Anorexia', 'Arson', 'Fascination with Fire', 'Fingernail Biting', 'Hair Twisting/Pulling'], None), ('Witchcraft / Occult', ['Ouija', 'Palmistry', 'Halloween', 'Familiar Spirits (contacting the dead)', 'Spirit Guide', 'Divination', 'Sorcery', 'Python (divination that chokes prayer)', 'Horoscopes', 'Astrology', 'Fortune-Telling', 'Tea Leaves', 'Worship of the Dead', 'Charms', 'Crystals', 'Pyramids', 'Tarot Cards', 'Pendulum', 'Voodoo', 'Wicca', 'Santería', 'Medicine Man Spirits', 'Native or Tribal Witchcraft', 'Shamanism', 'Psychic', 'Séance', 'Astral Projection', 'Witchcraft Control', 'Harry Potter', 'Reiki', 'Energy Healing', 'Chakras', 'Manifesting', 'Law of Attraction', 'Psychedelics', 'Ayahuasca', 'Hypnosis', 'Ghost Hunting', 'Spells', 'Satanism', 'Occult Objects in the Home', 'Nephilim (the giants of Genesis 6)'], None), ('Fear', ['of Abandonment', 'of Committing the Unpardonable Sin', 'of Losing Salvation', 'of Death', 'of Driving', 'of the Future', 'of Poverty', 'of Spiders', 'of Insects', 'of Snakes', 'of Man', 'of Woman', 'of People', 'of Animals', 'of Going Outside', 'of Disapproval', 'Not Good Enough', 'of Confrontation', 'of Success', 'of Germs', 'of Sickness', 'of Rejection', 'of Public Speaking', 'of Authority', 'of Doctors', 'of the Dark', 'of Satan', 'of Trusting', 'of Heights', 'of Love', 'of Loneliness', 'of Commitment', 'of Being Hurt', 'of Failure', 'All Phobias', 'Panic Attacks'], 'Other fears'), ('Heaviness / Stress', ['Depression', 'Grief', 'Sorrow', 'Sadness', 'Hopelessness', 'Worry', 'Entrapment', 'Anxiety', 'Nervousness', 'Stress', 'Pressure', 'Tension', 'Crying', 'Heartache', 'Defeatism', 'Unloving', 'Self-Pity', 'Pouting', 'Emotional Pain', 'Despair', 'Disappointment', 'Loneliness'], None), ('Jezebel (seduction and control)', ['Seductive Behavior', 'Witchcraft', 'Manipulation', 'Control'], None), ('Leviathan', ['Twisting Words', 'Pride', 'Blocks the Mind', 'Difficulty Studying the Bible'], None), ('Pride', ['Haughtiness', 'Ego', 'Vanity', 'Intellectualism', 'Leviathan', 'Self-Righteousness', 'Importance', 'Spiritual Pride', 'Arrogance'], None), ('Idolatry (false god)', ['Self (judgment sets itself up as god)', 'People', 'Pets', 'Things', 'Money', 'Hobbies', 'Games', 'Sports', 'Business', 'Work', 'Computer', 'Social Media', 'Phone', 'Screens', 'Lifestyle', 'Entertainment', 'TV', 'Problems', 'Sickness', 'Native American Ways', 'Food', 'Sex', 'Alcohol', 'Drugs', 'Past'], None), ('Lying', ['To Others', 'Exaggeration', 'To Self', 'Demons of the lies', 'Satanic lie program'], None), ('Mental Illness', ['Psychosis (losing touch with reality)', 'Mania', 'Attention-Deficit/Hyperactivity Disorder (ADHD)', 'Intellectual Disability', 'Deaf & Mute', 'Schizophrenia', 'Bipolar (formerly Manic Depression)', 'Borderline Personality Disorder (BPD)', 'Post-Traumatic Stress Disorder (PTSD)', 'Obsessive-Compulsive Disorder (OCD)', 'Paranoia', 'Hallucinations'], None), ('Dissociative Identity (DID, formerly MPD)', ['Alternate Personalities (Alters)', 'Voices'], None), ('Religion / Religious', ['Acupuncture', 'Doctrines', 'Ritualism', 'Tradition', 'False Prophet Spirit', 'Freemasonry', 'Eastern Star', 'Legalism', 'Formalism', 'KKK', 'Martial Arts', 'False Religions', 'Secret Societies', 'Illuminati', 'Yoga and the Kundalini Spirit'], None), ('Self', ['Selfishness', 'Self-Gratification', 'Self-Will', 'Self-Righteousness'], None), ('Stealing (Kleptomania)', ['Cheating'], None), ('Strife', ['Conflict', 'Bickering', 'Political Argument', 'Quarreling', 'Religious Meanness', 'Cruelness', 'Fighting', 'Criticism', 'Mockery', 'Folly', 'Coarse Joking', 'Gossip', 'Faultfinding', 'Judgment', 'Accusation'], None), ('Torment', ['Harassment', 'Nightmares', 'Sleep Paralysis', 'Night Terrors', 'Sensing an Evil Presence', 'Seeing or Hearing Demons'], None), ('Fatigue', ['Tiredness', 'Laziness', 'Insomnia', 'Despondency', 'Weakness', 'Lethargy', 'Sleepiness', 'Slumbering', 'Old and Tired'], None), ('Doubt / Disbelief', ['Skepticism', 'Unbelief'], None), ('False Compassion & Responsibility', ['Co-dependency', 'Need to Rescue / False Burden'], None), ('False Prophecy', ['False Voices'], None), ('Poverty', ['Financial Bondage', 'Blockage', 'Destruction', 'Cash Stealing', 'Lack', 'Stingy', 'Scarcity Mindset'], None), ('Profanity', ['Cursing', 'Blasphemy', 'Taking God’s Name in Vain'], None), ('Infirmity', ['Demon of Symptoms'], 'Any disease, sickness or symptom you have (its medical name, or what you feel)'), ('Perversion', ['Lust', 'Fornication', 'Fantasy', 'Sadistic', 'Lesbianism', 'Homosexuality', 'Masturbation', 'Adultery', 'Abuse of Children', 'Molestation', 'Pedophile', 'Incest', 'Rape', 'Incubus, Succubus (sexual attacks in dreams or at night)', 'Harlotry', 'Exposure', 'Bestiality', 'Pornography'], None)]  # from the Problem Checklist PDF (downloads/src/problem-checklist.html)

def _pl_item(t):
    # "Familiar Spirits (contacting the dead)" -> name plus a small gloss
    m = re.match(r'^(.*?)\s*\(([^)]*\s[^)]*)\)$', t)
    if m and not m.group(2).isupper():
        return f'{H.escape(m.group(1))} <span class="gl">({H.escape(m.group(2))})</span>'
    return H.escape(t)

def problem_list():
    rows = []
    for g, items, other in PROBLEMS:
        sub = ''.join(f'<label class="ck"><input type="checkbox" value="{H.escape(t)}"> {_pl_item(t)}</label>' for t in items)
        if other:
            sub += f'<label class="ot">{H.escape(other)}</label><input type="text" class="pt">'
        n = len(items)
        rows.append(f'<div class="pg"><div class="ph"><label class="ck gh"><input type="checkbox" class="pgc" value="{H.escape(g)}"> {_pl_item(g)}</label>'
                    f'<button type="button" class="pm" data-n="{n}" aria-expanded="false">{n} more</button></div><div class="pi" hidden>{sub}</div></div>')
    return ('<fieldset class="plist"><legend>What would you like freedom from?</legend>'
            '<p class="small">Check any area that is a problem for you now, or that has followed you through life. '
            'Tap <b>more</b> to see the details under each one and check those too. Check as many as apply. '
            'This list is kept confidential and helps your minister prepare.</p>'
            '<p class="pray small"><b>Pray first:</b> Father God, search me and know my heart; try me and know my thoughts. '
            'Holy Spirit, show me anything in me that is not of You. Help me to be honest and unafraid, and lead me in the everlasting way. '
            'In Jesus&rsquo; name, amen. <span class="ref">Based on Psalm 139:23-24</span></p>'
            '<div class="pgrid">' + ''.join(rows) + '</div>'
            '<label class="ot">Anything else not listed</label><textarea class="pt" data-l="Anything else"></textarea>'
            '<input type="hidden" name="Problems checked"></fieldset>')

PLIST_JS = """<script>(function(){
document.addEventListener('click',function(e){var b=e.target.closest('.pm');if(!b)return;var pi=b.closest('.pg').querySelector('.pi');pi.hidden=!pi.hidden;b.setAttribute('aria-expanded',!pi.hidden);b.textContent=pi.hidden?b.dataset.n+' more':'Hide';});
document.addEventListener('change',function(e){var t=e.target,g=t.closest('.pg');if(!g)return;var c=g.querySelector('.pgc');
 if(t===c){if(c.checked){var b=g.querySelector('.pm'),pi=g.querySelector('.pi');if(pi.hidden)b.click();}else{g.querySelectorAll('.pi input[type=checkbox]').forEach(function(x){x.checked=false})}}
 else if(t.checked||(t.type==='text'&&t.value.trim()))c.checked=true;});
document.addEventListener('submit',function(e){var f=e.target,h=f.querySelector('input[name="Problems checked"]');if(!h)return;var out=[];
 f.querySelectorAll('.pg').forEach(function(g){var c=g.querySelector('.pgc'),s=[];g.querySelectorAll('.pi input[type=checkbox]:checked').forEach(function(x){s.push(x.value)});
  var o=g.querySelector('.pi .pt');if(o&&o.value.trim())s.push('other: '+o.value.trim());if(c.checked||s.length)out.push(c.value+(s.length?': '+s.join(', '):''));});
 var a=f.querySelector('textarea.pt');if(a&&a.value.trim())out.push('Anything else: '+a.value.trim());
 h.value=out.length?out.join('\\n'):'(none checked)';},true);
})();</script>"""

ANYWHERE = f'''
<section class="page-hero"><div class="wrap">
<h1>Help from anywhere</h1>
<p>Can't come on a Monday? Three simple steps at home, then a trained minister meets with you by phone, Zoom or FaceTime. It's free.</p>
<p class="small">Open to people anywhere in the world. Our ministers mainly speak English. If you would prefer another language, tell us which one on the form, and we will look for a minister who speaks it.</p>
</div></section>
<section><div class="wrap">
<div class="progress"><span>1 Learn</span><span>2 Close the doors</span><span>3 Request a minister</span></div>

<div class="stepcard"><div class="n">1</div><div><h3>Learn what deliverance is</h3><p>Read this short introduction: what deliverance is, why believers still need it, and what to expect.</p>
<p><a class="btn" href="{IMG}downloads/introduction-to-deliverance.pdf">Introduction to Deliverance</a> <span class="muted small">2 pages · PDF</span> <a class="es" lang="es" href="{IMG}downloads/es/introduccion-a-la-liberacion.pdf">En español</a></p></div></div>

<div class="stepcard"><div class="n">2</div><div><h3>Pray the door-closing prayer <span class="pill">required</span></h3>
<p>Until you meet with a minister, this prayer is a good place to begin. It doesn't replace one-on-one deliverance, but it lets you start shutting doors the enemy may have used and stand on what Jesus has already done for you while you wait.</p>
<p>Pray it aloud as the video leads you, using the <a href="{UP}brown-handout-4-11.pdf">door-closing prayer handout</a>. The <a href="{IMG}downloads/door-closing-prayer.pdf">Door-Closing Prayer at a glance</a> outlines each part of the prayer on two pages, so you can see where you are and come back to it. <a class="es" lang="es" href="{IMG}downloads/es/oracion-para-cerrar-puertas.pdf">En español</a></p>
{yt("9CH5Lc2y9bQ","The door-closing prayer","31 min")}</div></div>

<div class="stepcard"><div class="n">3</div><div><h3>Request a minister</h3><p>Tell us how to reach you and check the areas where you want freedom.</p>
{form("Request a session", NAME_EMAIL + LANG + '<div><label>How would you like to meet?</label><select><option>Phone call</option><option>Zoom</option><option>FaceTime</option></select></div><div><label>What is the main reason you are seeking deliverance ministry?</label><textarea placeholder="In a few words or a few sentences, whatever is on your heart"></textarea></div>' + problem_list(), "Request a session")}
{PLIST_JS}</div></div>

<div class="stepcard next"><div class="n">&#10003;</div><div><h3>What happens next</h3><p>A minister will reach out to you to schedule your deliverance session by phone, Zoom or FaceTime. Until then, keep praying the door-closing prayer, and rest in this: “Come to me, all you who labor and are heavily burdened, and I will give you rest.” <span class="ref">Matthew 11:28</span></p></div></div>
</div></section>
'''

# ---------------- CHILDREN ----------------
CHILDREN = f'''
<section class="page-hero"><div class="wrap">
<h1>Help for your child</h1>
<p>“Allow the little children, and don't forbid them to come to me; for the Kingdom of Heaven belongs to ones like these.” <span class="ref">Matthew 19:14</span></p>
</div></section>
<section><div class="wrap two">
<div>
<h2>How it works</h2>
<ol class="steps">
<li><b>Parents first.</b> A parent or guardian receives ministry before their child does, on a Monday night or <a href="help-anywhere.html">from anywhere</a>.</li>
<li><b>Request an appointment</b> for your child, ages 14 and younger, within 1 to 4 weeks after your own ministry.</li>
<li><b>Minister together.</b> A parent stays with their child throughout.</li>
</ol>
<p class="muted">There is no childcare on Monday nights, so please don't bring children to the general meeting.</p>
<h2>Learn more first</h2>
{yt("sIxPRqK1f8M","Ministering to children")}
</div>
<div>
{form("Request an appointment for your child", NAME_EMAIL + LANG + '<div class="row2"><div><label>Child\'s age</label><input type="number" min="0" max="14"></div><div><label>When did you receive ministry?</label><input type="date"></div></div><div><label>Anything we should know? (optional)</label><textarea></textarea></div>', "Request appointment")}
</div>
</div></section>
'''

# ---------------- LEARN ----------------
LEARN = f'''
<section class="page-hero"><div class="wrap">
<h1>Learn to minister</h1>
<p>“He called the twelve together, and gave them power and authority over all demons, and to cure diseases.” <span class="ref">Luke 9:1</span> Every believer can learn to minister healing and freedom. All training here is free.</p>
</div></section>
<section><div class="wrap">
<div class="path"><div><b>1</b> Receive ministry yourself</div><div><b>2</b> Take the basic course</div><div><b>3</b> Observe on Monday nights</div><div><b>4</b> Minister with a team</div></div>

<h2>Basic training course</h2>
<div class="vgrid">
{yt("RbJxPjfCSQ4","Basic training: overview")}
{yt("QK77LckG2Dc","Session 1")}
{yt("ULodG3cZvGk","Session 2")}
{yt("IVFJVK-i1Nc","Session 3")}
{yt("-lYG-ujn_-k","Session 4")}
{yt("jEWW06M4kh0","Session 5")}
</div>

<h2>Topical teaching</h2>
<div class="vgrid">
{yt("sIxPRqK1f8M","Ministering to children")}
{yt("oe-wjHLrmyg","Witchcraft")}
{yt("hNFjBEM5yIs","Yoga: its truth and deceptions")}
</div>

<div class="two">
<div class="card soft"><h3>Free handouts and downloads</h3>
<p>Free to download, print and share.</p>
<ul class="dl">
<li><a href="{IMG}downloads/introduction-to-deliverance.pdf">Introduction to Deliverance</a> <a class="es" lang="es" href="{IMG}downloads/es/introduccion-a-la-liberacion.pdf">En español</a> <span class="muted">2 pages · what deliverance is</span></li>
<li><a href="{IMG}downloads/who-i-am-in-christ.pdf">Who I Am in Christ</a> <a class="es" lang="es" href="{IMG}downloads/es/quien-soy-en-cristo.pdf">En español</a> <span class="muted">1 page · say five each day</span></li>
<li><a href="{IMG}downloads/problem-checklist.pdf">Problem Checklist</a> <a class="es" lang="es" href="{IMG}downloads/es/lista-de-problemas.pdf">En español</a> <span class="muted">2 pages · fill out before your session</span></li>
<li><a href="{IMG}downloads/follow-up-for-recipients.pdf">You Don&rsquo;t Walk This Alone</a> <a class="es" lang="es" href="{IMG}downloads/es/no-camina-solo-en-esto.pdf">En español</a> <span class="muted">3 pages · after your session</span></li>
<li><a href="{IMG}downloads/follow-up-for-ministers.pdf">Follow-Up for Ministers</a> <a class="es" lang="es" href="{IMG}downloads/es/seguimiento-para-ministros.pdf">En español</a> <span class="muted">4 pages · staying in touch</span></li>
<li><a href="{IMG}downloads/door-closing-prayer.pdf">Door-Closing Prayer (at a glance)</a> <a class="es" lang="es" href="{IMG}downloads/es/oracion-para-cerrar-puertas.pdf">En español</a> <span class="muted">2 pages · minister&rsquo;s guide to lead the prayer</span></li>
<li><a href="{IMG}downloads/the-importance-of-forgiveness.pdf">The Importance of Forgiveness</a> <a class="es" lang="es" href="{IMG}downloads/es/la-importancia-del-perdon.pdf">En español</a> <span class="muted">19 pages · Scripture study</span></li>
</ul>
<p class="muted">More prayers, renunciations, and the CD and DVD training sets are being converted. {tbc("coming soon")}</p></div>
<div class="card soft book"><div><h3>Founder Everett Cox&rsquo;s book</h3>
<p><i>Doing the Supernatural Works of Jesus</i>, the ministry's training manual.</p>
<p><a class="btn ghost" href="https://a.co/d/03yBlejH" target="_blank" rel="noopener">Get the book on Amazon</a></p></div>
<a href="https://a.co/d/03yBlejH" target="_blank" rel="noopener"><img src="{IMG}book-cover.jpg" width="800" height="1143" alt="Cover of Doing the Supernatural Works of Jesus by Everett E Cox"></a></div>
</div>

<h2>Join the Monday team</h2>
<p>New team members receive ministry, complete the basic course, then observe and serve alongside experienced ministers.</p>
{form("I'm interested in training", NAME_EMAIL + '<div><label>Have you received ministry here?</label><select><option>Yes</option><option>Not yet</option></select></div>', "Send")}
</div></section>
'''

# ---------------- CHURCHES ----------------
CHURCHES = f'''
<section class="page-hero"><div class="wrap">
<h1>For churches and groups</h1>
<p>“He gave some to be … shepherds and teachers; for the perfecting of the saints, to the work of serving, to the building up of the body of Christ.” <span class="ref">Ephesians 4:11-12</span></p>
</div></section>
<section><div class="wrap two">
<div>
<h2>We come alongside shepherds</h2>
<p>A ministry team can visit your church, home group or conference to serve your people and equip your leaders.</p>
<div class="offer"><h3>Teaching</h3><p>An introduction to deliverance, healing and the gifts of the Spirit, rooted in Scripture.</p></div>
<div class="offer"><h3>Ministry sessions</h3><p>Group and one-on-one deliverance and healing for your members.</p></div>
<div class="offer"><h3>Training</h3><p>Equip your own leaders to minister, so the work continues after we leave.</p></div>
<p class="muted">There is no fee. Love offerings are welcome but never required.</p>
</div>
<div>
{form("Invite a team", NAME_EMAIL + '<div><label>Church or group</label><input type="text"></div><div><label>What are you hoping for?</label><select><option>Teaching</option><option>Ministry sessions</option><option>Training our leaders</option><option>Not sure yet</option></select></div><div><label>Possible dates (optional)</label><input type="text"></div>', "Send invitation")}
</div>
</div></section>
'''

# ---------------- TESTIMONIES ----------------
T = [
 ("Healing", [("Back and neck healing","backs-necks.mp3"),("A doctor's back healed","DrKellyBackHealing.mp3"),("Relief from a frozen neck","frozen-up-neck.mp3"),("Cured of deafness","betty-bright-deafness.mp3"),("Lupus healed with Jesus","lupus-healed.mp3"),("Lupus and a heart attack","LupusHeartAttack.mp3"),("Victory over heart attacks","heart-attack-spirits-jmccormick.mp3"),("Seizures","Seizures.mp3"),("Infirmity","Infirmity.mp3"),("Eight healing testimonies","8_Healing_Testimonies.mp3"),("Medical doctors","MedicalDoctors.mp3")]),
 ("Fear and anxiety", [("Set free from fear","SetFreeFromFear.mp3"),("Many fears","many-fears.mp3"),("Drugs, panic attacks and healing","drugs-panicattacks-healing.mp3")]),
 ("Addictions and compulsions", [("Addictions","Addictions.mp3"),("Redemption over cocaine and illiteracy","cocain-illiteracy.mp3"),("Bulimia and anorexia","Bulimia_Anorexia.mp3"),("Smoking and anger","DrBillHodgsonSmokingAnger.mp3"),("Homosexuals set free","HomosexualsSetFree.mp3")]),
 ("Marriage and family", [("Marriage restored through deliverance","marriages-restored.mp3"),("Children","Children.mp3"),("A child set free","Twitchellchild.mp3"),("A granddaughter's story","GranddaughterEC.mp3")]),
 ("The occult and spiritual darkness", [("Psychics, astrologers and Harry Potter","PsychicsAstrologersHarryPotter.mp3"),("A haunted house","HauntedHouse.mp3"),("Safety from hospital ghosts","hospital-ghosts.mp3"),("Native American heritage","NativeAmerican.mp3")]),
 ("Ministers' stories", [("Interview: a minister's journey","ECInterviewMaryJo.mp3")]),
]
cnt = sum(len(x) for _,x in T)
# One description per recording; fill these in as each one is listened to.
DESC = {}
LOREM = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore."
TBODY = "".join(f'<h2>{g}</h2><div class="audios">' + "".join(f'<div class="audio"><b>{t}</b><p class="desc">{DESC.get(f, LOREM)}</p><audio controls preload="none" src="{UP}{f}"></audio></div>' for t,f in items) + '</div>' for g,items in T)
TESTIMONIES = f'''
<section class="page-hero"><div class="wrap">
<h1>Testimonies</h1>
<p>{cnt} people share, in their own voices, what Jesus has done. Free to listen, download and share. To save one, use the download option in its player.</p>
</div></section>
<section><div class="wrap">
<h2>David&rsquo;s testimony</h2>
<div class="card soft story"><p>“I confessed Christ and was baptized at about thirteen, then went back to my worldly ways. It took me decades to see how off-course I had become and the battle I had been ignoring. I attended church in spurts, prayed generic prayers and hoped for the best. Satan didn’t have to attack me hard because in my sin I was neutralized. I was having no impact for the Kingdom. At one point I didn’t even call myself a Christian. I called myself agnostic – I believed in a creator and because of my upbringing I worshipped it as a Christian, not knowing a generic creator isn’t the God of the Bible. I preferred the notion of Thomas Jefferson’s Bible that had all the supernatural cut out.</p>
<p>“That changed one day in 2017, when Jesus told me that I either believe all of the Bible or none of it. He gave me a vision of myself straddling a fence, needing to pick a side. It felt like an ultimatum, a now-or-never moment. I chose to believe it all. I flipped open my Bible and it opened to John 14. My eyes fell on verse 6, ‘Jesus said to him, “I am the way, the truth, and the life. No one comes to the Father except through Me.”’ (NKJV) I couldn’t ignore it and began changing my beliefs.</p>
<p>“That’s when the attacks started. I was un-armed cannon fodder in a bloody war. The attacks intensified, manifesting in ways I could not rationalize away. That opened my eyes to the ‘supernatural’ – the spiritual realm. But as the attacks continued, awareness alone was more frightening than helpful. Then, through guidance from strong, experienced spiritual warriors, Jesus began to show me who I am in Him, and what He had given me to fight with. Now my mission is to keep growing as a spiritual warrior, to help others in their spiritual struggles, and to train those willing to pick up their cross and fight the good fight for God’s Kingdom.”</p>
<p class="sig">&mdash; David</p></div>
{TBODY}
</div></section>
'''

# ---------------- GIVE ----------------
GIVE = f'''
<section class="page-hero"><div class="wrap">
<h1>Give</h1>
<p>“Freely you received, so freely give.” <span class="ref">Matthew 10:8</span> No one is ever charged for ministry. Your gifts keep it that way.</p>
</div></section>
<section><div class="wrap">
<div class="givegrid">
<div class="card"><h3>Give online</h3><p>One-time or monthly, by card or PayPal.</p><form action="https://www.paypal.com/cgi-bin/webscr" method="post" target="_blank"><input type="hidden" name="cmd" value="_s-xclick"><input type="hidden" name="hosted_button_id" value="Z3A55CQMYUGSG"><button class="btn" type="submit">Give online</button></form><p class="small muted">Opens PayPal in a new tab.</p></div>
<div class="card"><h3>Give by check</h3><p>Payable to Deliverance Ministries Inc<br>2828 NW 57th, Ste. 305<br>Oklahoma City, OK 73112</p></div>
<div class="card"><h3>Where it goes</h3><ul class="check"><li>Free Monday night ministry</li><li>Free phone, Zoom and FaceTime sessions</li><li>Free training and downloads</li><li>Visits to churches and groups</li></ul></div>
</div>
<p class="center muted">“Let each man give according as he has determined in his heart, not grudgingly or under compulsion, for God loves a cheerful giver.” <span class="ref">2 Corinthians 9:7</span></p>
<p class="center small muted">Deliverance Ministries Inc is a 501(c)(3) nonprofit organization. Gifts are tax-deductible as allowed by law.</p>
</div></section>
'''

# ---------------- ABOUT ----------------
ABOUT = f'''
<section class="page-hero"><div class="wrap">
<h1>About the ministry</h1>
<p class="lead">This is the enduring ministry of Jesus Christ.</p>
</div></section>
<section><div class="wrap narrow">
<p>Jesus healed the sick and cast out demons, and He sent His followers to do the same: “Heal the sick, cleanse the lepers, and cast out demons. Freely you received, so freely give.” <span class="ref">Matthew 10:8</span> Deliverance Ministries exists to continue that work and to equip the body of Christ to carry it on.</p>
<p>Since 1984, teams of trained volunteer ministers in Oklahoma City have prayed with tens of thousands of people {tbc("figure?")} for freedom, inner healing and physical healing. Ministry has always been free.</p>
<h2>What we do</h2>
<ul class="check">
<li>Free one-on-one ministry every Monday night in Oklahoma City</li>
<li>Free ministry by phone, Zoom or FaceTime, with a guide to prepare at home</li>
<li>Free training for believers who want to minister</li>
<li>Teaching and ministry for churches and groups</li>
</ul>
<h2>What we believe</h2>
<div class="card soft"><p class="muted">Statement of faith {tbc("to come")}</p></div>
<h2>How we minister</h2>
<p>We teach before we minister. People forgive, repent and renounce what opened the door to the enemy, and then, in Jesus' name, we command evil spirits to leave and pray for healing. We work as teams, so no one ministers alone and the work never depends on one person.</p>
</div></section>
'''

# ---------------- CONTACT ----------------
CONTACT = f'''
<section class="page-hero"><div class="wrap">
<h1>Contact us</h1>
<p>Questions, prayer requests or anything else. Someone will reply personally.</p>
</div></section>
<section><div class="wrap two">
<div>
<p><b>Phone</b><br>(405) 842-5509</p>
<p><b>Email</b><br><a href="mailto:delmin.org@gmail.com">delmin.org@gmail.com</a></p>
<p><b>Mail</b><br>Deliverance Ministries Inc<br>2828 NW 57th, Ste. 305<br>Oklahoma City, OK 73112</p>
<p><b>Monday nights</b><br>9201 N. Rockwell, Oklahoma City, OK 73132</p>
</div>
<div>{form("Send a message", NAME_EMAIL + '<div><label>Message</label><textarea></textarea></div>', "Send")}</div>
</div></section>
'''

CSS = '''/* Deliverance Ministries draft: shared styles */
:root{--ink:#1c2830;--muted:#5b6a73;--line:#dbe2e5;--paper:#faf8f4;--card:#fff;--teal:#17394a;--teal2:#245566;--teal-soft:#e7f0f1;--gold:#c08a2b;--gold-soft:#fbf2df;
--sans:-apple-system,BlinkMacSystemFont,"Segoe UI","Helvetica Neue",Arial,sans-serif;--serif:Georgia,"Times New Roman",serif}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font:17px/1.6 var(--sans)}
img,svg,iframe{max-width:100%}
a{color:var(--teal2)}
h1,h2,h3{color:var(--teal);line-height:1.2}
h2{font-size:1.5rem;margin:1.6rem 0 .7rem}
h3{font-size:1.08rem;margin:0 0 .35rem}
p{margin:0 0 1rem}
.wrap{max-width:1040px;margin:0 auto;padding:0 18px}
.narrow{max-width:720px}
.center{text-align:center}
.muted{color:var(--muted)}.small{font-size:.86rem}
.ref{font-size:.8em;color:var(--muted);white-space:nowrap;font-style:normal}
.tbc{background:#fff1a8;color:#5c4a00;border-radius:4px;padding:0 5px;font-size:.85em;font-weight:600;white-space:nowrap}
.draftbar{background:#fff1a8;color:#3d3200;font-size:.84rem;text-align:center;padding:6px 12px}
.draftbar .tbc{background:#ffe066}
header.top{background:var(--teal);position:sticky;top:0;z-index:5}
header.top .wrap{display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px 16px;padding-top:8px;padding-bottom:8px}
.brand{display:flex;align-items:center;gap:10px;color:#fff;text-decoration:none;font-weight:700;font-size:1.08rem}
.brand svg{width:34px;height:34px;flex:none}
.brand path[stroke="#17394a"]{stroke:#17394a}
nav{display:flex;flex-wrap:wrap;gap:6px 16px;align-items:center}
nav a{color:#d9e7ea;text-decoration:none;font-size:.93rem;white-space:nowrap}
nav a:hover,nav a[aria-current]{color:#fff;text-decoration:underline;text-underline-offset:4px}
nav a.cta{background:var(--gold);color:#fff;padding:6px 14px;border-radius:999px;text-decoration:none}
.hero{background:linear-gradient(160deg,var(--teal) 0%,var(--teal2) 100%);color:#fff;text-align:center;padding:64px 0 56px}
.hero h1{color:#fff;font-family:var(--serif);font-size:clamp(2.1rem,6vw,3.3rem);margin:0 0 1rem}
.hero .lead{max-width:680px;margin:0 auto 1.2rem;font-size:1.12rem;color:#e6f0f2}
.hero blockquote{font-family:var(--serif);font-style:italic;font-size:1.15rem;margin:0 auto 1.6rem;color:#fff}
.hero .ref{color:#bcd3d8}
.page-hero{background:var(--teal);color:#e6f0f2;padding:40px 0 30px}
.page-hero h1{color:#fff;font-family:var(--serif);font-size:clamp(1.9rem,5vw,2.6rem);margin:0 0 .6rem}
.page-hero p{max-width:760px}.page-hero .ref{color:#bcd3d8}
.page-hero .lead{font-family:var(--serif);font-size:1.35rem;font-style:italic;color:#fff}
section{padding:28px 0}
.band{background:var(--teal-soft)}
.btn{display:inline-block;background:var(--gold);color:#fff;text-decoration:none;font-weight:700;padding:12px 24px;border-radius:999px;border:0;font-size:1rem;cursor:pointer}
.btn.ghost{background:transparent;color:var(--teal);border:2px solid var(--teal)}
.btn[disabled]{opacity:.55;cursor:not-allowed}
.personas{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.personas.three{margin-bottom:24px}
.persona{display:flex;flex-direction:column;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:20px;text-decoration:none;color:var(--ink);transition:box-shadow .15s,transform .15s}
.persona:hover{box-shadow:0 6px 20px rgba(23,57,74,.14);transform:translateY(-2px)}
.persona svg{width:44px;height:44px;margin-bottom:10px}
.persona p{color:var(--muted);flex:1}
.go{color:var(--gold);font-weight:700}
.two{display:grid;grid-template-columns:1fr 1fr;gap:28px;align-items:start}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:20px;margin:0 0 18px}
.card.soft{background:var(--gold-soft);border-color:#ecd9a6}
.card.quote p{font-family:var(--serif);font-style:italic;font-size:1.1rem}
.timeline{list-style:none;padding:0;margin:0 0 1rem;border-left:3px solid var(--gold)}
.timeline li{padding:4px 0 10px 16px}
.timeline b{display:inline-block;min-width:74px;color:var(--teal)}
.pill{display:inline-block;background:var(--teal);color:#fff;font-size:.72rem;font-weight:700;border-radius:999px;padding:1px 9px;vertical-align:middle}
.steps{padding-left:22px}.steps li{margin-bottom:8px}
.check{list-style:none;padding:0}.check li{padding-left:26px;position:relative;margin-bottom:6px}
.check li:before{content:"✓";position:absolute;left:4px;color:var(--gold);font-weight:700}
.progress{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:20px}
.progress span{background:var(--teal-soft);color:var(--teal);font-size:.82rem;font-weight:700;border-radius:999px;padding:4px 12px}
.stepcard{display:grid;grid-template-columns:44px 1fr;gap:14px;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:18px;margin-bottom:16px}
.stepcard .n{width:40px;height:40px;border-radius:50%;background:var(--gold);color:#fff;font-weight:800;display:flex;align-items:center;justify-content:center;font-size:1.1rem}
.stepcard .form{margin-top:10px;background:var(--paper)}
.video{margin:8px 0 12px}
.frame{position:relative;padding-top:56.25%;border-radius:10px;overflow:hidden;background:#0d1f28}
.frame iframe{position:absolute;inset:0;width:100%;height:100%;border:0}
figcaption{font-size:.9rem;font-weight:600;color:var(--teal);margin-top:6px}
.len{color:var(--muted);font-weight:400;margin-left:6px}
.vgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.path{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:6px 0 10px}
.path div{background:var(--teal);color:#fff;border-radius:10px;padding:12px;font-weight:600;font-size:.92rem}
.path b{display:inline-flex;width:24px;height:24px;border-radius:50%;background:var(--gold);align-items:center;justify-content:center;margin-right:6px}
.offer{border-left:4px solid var(--gold);padding:2px 0 2px 14px;margin-bottom:14px}
.dl{list-style:none;padding:0;margin:8px 0}.dl li{padding:7px 0;border-bottom:1px solid rgba(0,0,0,.08)}.dl a{font-weight:700}.dl .muted{display:block;font-size:.88em}.dl a.es{font-weight:600;font-size:.82em;margin-left:8px;padding:1px 8px;border:1px solid currentColor;border-radius:10px;white-space:nowrap}
.story p{font-style:italic}.story .sig{font-style:normal;font-weight:700;margin:0}
.book img{display:block;width:100%;height:auto;margin-top:14px;border-radius:4px;box-shadow:0 4px 12px rgba(0,0,0,.25)}
.offer p{margin:0}
.audios{display:grid;grid-template-columns:repeat(2,1fr);gap:12px}
.audio{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px 14px}
.audio b{display:block;color:var(--teal);margin-bottom:2px}
.audio .desc{font-size:.88rem;color:var(--muted);margin:0 0 8px}
.audio audio{width:100%}
.givegrid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.form label{display:block;font-size:.88rem;font-weight:600;margin:0 0 4px;color:var(--teal)}
.form input,.form select,.form textarea{width:100%;font:inherit;font-size:.95rem;padding:9px 10px;border:1px solid var(--line);border-radius:8px;background:#fff;margin-bottom:12px}
.form textarea{min-height:80px}
.row2{display:grid;grid-template-columns:1fr 1fr;gap:0 12px}
.note{font-size:.85rem;color:#5c4a00;background:#fff1a8;border-radius:6px;padding:5px 9px}
footer{background:var(--teal);color:#cfe0e4;padding:30px 0 20px;margin-top:20px;font-size:.92rem}
footer a{color:#fff}footer b{color:#fff}
.fgrid{display:grid;grid-template-columns:2fr 1fr 1.3fr;gap:20px}
footer .ref{color:#a9c4ca}
@media (max-width:820px){.personas,.vgrid,.givegrid{grid-template-columns:1fr 1fr}.two{grid-template-columns:1fr}.path{grid-template-columns:1fr 1fr}.fgrid{grid-template-columns:1fr}}
@media (max-width:560px){body{font-size:16px}.personas,.vgrid,.givegrid,.audios,.row2{grid-template-columns:1fr}nav a{font-size:.86rem}.hero{padding:44px 0 40px}.stepcard{grid-template-columns:1fr}.path{grid-template-columns:1fr}}
'''

# ---------------- COMBINED (Lambs to Lions look) ----------------
HOME2 = f'''
<section class="hero split"><div class="wrap">
<figure class="hero-img"><img src="../freedom.jpg" srcset="../freedom-700.jpg 700w, ../freedom.jpg 1200w" sizes="(max-width:820px) 100vw, 460px" width="1200" height="1200" alt="A man kneels with arms raised toward a cross as his chains break."></figure>
<div class="hero-text">
<h1>Freedom and healing in Jesus Christ</h1>
<div class="verses">
<p>“If therefore the Son makes you free, you will be free indeed.” <span class="ref">John 8:36</span></p>
<p>The Father “delivered us out of the power of darkness, and translated us into the Kingdom of the Son of his love.” <span class="ref">Colossians 1:13</span></p>
<p>“Stand firm therefore in the liberty by which Christ has made us free, and don’t be entangled again with a yoke of bondage.” <span class="ref">Galatians 5:1</span></p>
</div>
<a class="btn" href="#help">Find the help that fits you</a><a class="btn ghost" href="about.html">About the ministry</a>
</div>
</div></section>

<section><div class="wrap narrow">
<p class="lead">Depression, fear, addiction, illness, guilt, heartache or trauma don’t have to have the last word. <b>Jesus still sets people free today,</b> and every ministry session here is free of charge.</p>
</div></section>

<section id="help" class="alt"><div class="wrap">
<h2 class="center">How can we help you?</h2>
<div class="personas">{PERSONAS}</div>
</div></section>

<section><div class="wrap">
<h2 class="center">What happens in ministry</h2>
<ol class="strip">
<li><b>Learn</b>what Jesus did and still does</li>
<li><b>Close the doors</b>forgive, repent, renounce</li>
<li><b>Soul ties</b>break ungodly ties</li>
<li><b>Inner healing</b>for past wounds</li>
<li><b>Deliverance</b>evil spirits leave in Jesus’ name</li>
<li><b>Healing</b>prayer for the body</li>
<li><b>Stay free</b>walk in the Spirit</li>
</ol>
</div></section>

<section class="alt"><div class="wrap two">
<div>
<h2>Monday nights in Oklahoma City</h2>
<ol class="timeline">
<li><b>5:30 pm</b> Introduction and teaching</li>
<li><b>6:30 pm</b> Door-closing prayer, together <span class="pill">required</span></li>
<li><b>7:30 pm</b> Personal ministry, ending by 10:30 pm at the latest</li>
</ol>
<p>9201 N. Rockwell, Oklahoma City, OK 73132<br><span class="muted">West side of Rockwell, between NW Expressway and Britton Rd.</span></p>
<p>Everyone is welcome, whether you live nearby or travel to come.</p>
<a class="btn" href="help-nearby.html">Plan your visit</a>
</div>
<div>
<blockquote class="v">“The Spirit of the Lord is on me, because he has anointed me to preach good news to the poor. He has sent me to heal the broken hearted, to proclaim release to the captives, recovering of sight to the blind, to deliver those who are crushed.” <span class="ref">Luke 4:18</span></blockquote>
<div class="grid2">
<div class="box won"><span class="lbl">Hear what God has done</span><p>Nearly thirty people share, in their own voices, what Jesus has done.</p><a href="testimonies.html">Listen to testimonies →</a></div>
<div class="box navy"><span class="lbl">Always free</span><p>Trained volunteer ministers, carried by the gifts of people set free.</p><a href="give.html">Support the ministry →</a></div>
</div>
</div>
</div></section>

<section class="cta-band"><div class="wrap">
<h2>Ready to experience the freedom God has for you?</h2>
<p><i>“Freely you received, so freely give.”</i> <span class="ref">Matthew 10:8</span></p>
<a class="btn" href="get-help.html">Get help</a><a class="btn ghost" href="give.html">Give</a>
</div></section>
'''

CSS2 = '''/* Deliverance Ministries draft. Palette: the logo burgundy #5f0423 (one shade only) with a muted tan accent #c9a97c */
:root{--ink:#2b1a20;--muted:#6e5a60;--line:#e3d8c6;--paper:#f5efe4;--card:#fff;
--navy:#5f0423;--navy-soft:#f4ece0;--gold:#c9a97c;--gold-soft:#f4ece0;--gold-line:#dccaa8;
--wine:#5f0423;--wine-soft:#f4ece0;--sage:#5f0423;--sage-soft:#f4ece0;
--serif:Georgia,"Times New Roman",serif;--sans:-apple-system,BlinkMacSystemFont,"Segoe UI","Helvetica Neue",Arial,sans-serif}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--paper);color:var(--ink);font:18px/1.6 var(--serif)}
img,svg,iframe{max-width:100%}
a{color:var(--navy)}
h1,h2,h3,nav,label,.btn,.lbl,.pill,.go,figcaption,footer,.draftbar,.progress,.strip,.timeline b,.tbc,.note{font-family:var(--sans)}
h1,h2,h3{color:var(--navy);line-height:1.25}
h2{font-size:1.55rem;margin:0 0 .7rem}
h3{font-size:1.1rem;margin:0 0 .35rem}
p{margin:0 0 1rem}
.wrap{max-width:1000px;margin:0 auto;padding:0 20px}
.narrow{max-width:720px}
.center{text-align:center}
.muted{color:var(--muted)}.small{font-size:.86rem}
.ref{font-family:var(--sans);font-size:.78em;color:var(--muted);white-space:nowrap;font-style:normal}
.tbc{background:#fff1a8;color:#5c4a00;border-radius:4px;padding:0 5px;font-size:.8em;font-weight:600;white-space:nowrap;font-style:normal}
.draftbar{background:#fff1a8;color:#3d3200;font-size:.84rem;text-align:center;padding:6px 12px}
.draftbar a{color:#3d3200}
header.top{background:var(--navy);position:sticky;top:0;z-index:5}
header.top .wrap{display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px 16px;min-height:60px;padding-top:6px;padding-bottom:6px}
.brand{display:flex;align-items:center;gap:10px;color:#fff;text-decoration:none;font-family:var(--sans);font-weight:700;font-size:1.05rem;letter-spacing:.02em}
.brand svg,.brand img{width:40px;height:40px;flex:none}
nav{display:flex;flex-wrap:wrap;gap:6px 16px;align-items:center}
nav a{color:#ffffff;text-decoration:none;font-size:.92rem;white-space:nowrap}
nav a:hover,nav a[aria-current]{color:#fff;text-decoration:underline;text-underline-offset:4px}
nav a.cta{background:var(--gold);color:var(--navy);font-weight:700;padding:7px 14px;border-radius:999px;text-decoration:none}
.hero{background:var(--navy);color:#fff;padding:48px 0}
.hero h1{color:#fff;font-size:clamp(2.2rem,6vw,3.3rem);line-height:1.08;margin:0 0 1rem}
.hero.split .wrap{display:grid;grid-template-columns:1fr 1.05fr;gap:40px;align-items:center}
.hero.split .hero-img{order:2;margin:0}
.hero.split .hero-img img{display:block;width:100%;height:auto;border-radius:14px;box-shadow:0 18px 40px rgba(0,0,0,.35)}
.hero .verses{margin:0 0 1.6rem;border-left:3px solid var(--gold);padding-left:16px}
.hero .verses p{font-style:italic;font-size:1.02rem;line-height:1.5;color:#ffffff;margin:0 0 .7rem}
.hero .verses .ref{color:#e9dcc6}
.page-hero{background:var(--navy);color:#ffffff;padding:44px 0 36px;text-align:center}
.page-hero h1{color:#fff;margin:0 0 .6rem;font-size:clamp(1.9rem,6vw,2.7rem)}
.page-hero p{margin:.4rem auto 0;max-width:680px}
.page-hero .ref{color:#e9dcc6}
.page-hero .lead{font-style:italic;font-size:1.3rem;color:#fff}
section{padding:44px 0}
section.alt{background:#fff;border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.lead{font-size:1.15rem;text-align:center;max-width:720px;margin:0 auto}
.lead b{color:var(--wine);font-family:var(--sans)}
.btn{display:inline-block;background:var(--gold);color:var(--navy);text-decoration:none;font-weight:700;padding:13px 26px;border-radius:999px;font-size:1rem;border:0;cursor:pointer}
.btn:hover{filter:brightness(1.08)}
.btn.ghost{background:transparent;color:var(--navy);border:2px solid var(--navy)}
.hero .btn.ghost,.cta-band .btn.ghost{color:#fff;border-color:#fff;margin-left:8px}
.btn[disabled]{opacity:.55;cursor:not-allowed}
.personas{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:1.2rem}
.personas.three{margin-bottom:24px}
.persona{display:flex;flex-direction:column;background:var(--card);border:1px solid var(--line);border-top:4px solid var(--navy);border-radius:10px;padding:18px 20px;text-decoration:none;color:var(--ink);transition:box-shadow .15s,transform .15s}
.persona:hover{box-shadow:0 6px 20px rgba(95,4,35,.14);transform:translateY(-2px)}
.persona svg{width:44px;height:44px;margin-bottom:10px}
.persona svg [fill="#5f0423"]{fill:var(--navy)}
.persona svg [fill="#00622c"]{fill:var(--gold)}
.persona svg [stroke="#5f0423"]{stroke:var(--navy)}
.persona p{color:var(--muted);flex:1;font-size:.98rem}
.go{color:var(--navy);font-weight:700;font-size:.95rem}
.two{display:grid;grid-template-columns:1fr 1fr;gap:28px;align-items:start}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.box{border-radius:10px;padding:16px 18px}
.box p{font-size:.98rem}
.box .lbl{display:block;font-size:.78rem;letter-spacing:.12em;text-transform:uppercase;font-weight:700;margin-bottom:.35rem}
.box a{font-family:var(--sans);font-weight:700;font-size:.92rem}
.won{background:var(--sage-soft)}.won .lbl,.won a{color:var(--sage)}
.navy{background:var(--navy-soft)}.navy .lbl{color:var(--navy)}
blockquote.v{margin:0 0 1rem;padding:.8rem 1.1rem;background:var(--gold-soft);border-left:4px solid var(--gold);font-style:italic;border-radius:0 6px 6px 0}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:18px 20px;margin:0 0 18px}
.card.soft{background:var(--gold-soft);border-color:var(--gold-line)}
.card.quote p{font-style:italic}
.timeline{list-style:none;padding:0;margin:0 0 1rem;border-left:3px solid var(--gold)}
.timeline li{padding:4px 0 10px 16px}
.timeline b{display:inline-block;min-width:74px;color:var(--navy)}
.pill{display:inline-block;background:var(--navy);color:#fff;font-size:.72rem;font-weight:700;border-radius:999px;padding:1px 9px;vertical-align:middle}
.steps{padding-left:22px}.steps li{margin-bottom:8px}
ol.strip{list-style:none;padding:0;margin:1rem 0 0;display:grid;grid-template-columns:repeat(7,1fr);gap:8px;counter-reset:s}
ol.strip li{counter-increment:s;background:#fff;border:1px solid var(--line);border-top:4px solid var(--navy);border-radius:8px;padding:10px 8px;text-align:center;font-size:.85rem;line-height:1.3;color:var(--muted)}
ol.strip li::before{content:counter(s);display:block;width:26px;height:26px;margin:0 auto 6px;border-radius:50%;background:var(--navy);color:#fff;font-weight:700;line-height:26px}
ol.strip li b{display:block;color:var(--navy);font-size:.95rem;margin-bottom:2px}
.check{list-style:none;padding:0}.check li{padding-left:28px;position:relative;margin-bottom:6px}
.check li::before{content:"";position:absolute;left:0;top:6px;width:16px;height:16px;border:2px solid var(--navy);border-radius:3px;background:#fff}
.progress{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:20px}
.progress span{background:var(--navy-soft);color:var(--navy);font-size:.82rem;font-weight:700;border-radius:999px;padding:4px 12px}
.stepcard{display:grid;grid-template-columns:44px 1fr;gap:14px;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:18px;margin-bottom:16px}
.stepcard .n{width:40px;height:40px;border-radius:50%;background:var(--navy);color:#fff;font-family:var(--sans);font-weight:800;display:flex;align-items:center;justify-content:center;font-size:1.1rem}
.stepcard .form{margin-top:10px;background:var(--paper)}
.video{margin:8px 0 12px}
.frame{position:relative;padding-top:56.25%;border-radius:10px;overflow:hidden;background:#5f0423}
.frame iframe{position:absolute;inset:0;width:100%;height:100%;border:0}
figcaption{font-size:.9rem;font-weight:600;color:var(--navy);margin-top:6px}
.len{color:var(--muted);font-weight:400;margin-left:6px}
.vgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-bottom:1rem}
.path{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:6px 0 24px}
.path div{background:var(--navy);color:#fff;border-radius:10px;padding:12px;font-family:var(--sans);font-weight:600;font-size:.92rem}
.path b{display:inline-flex;width:24px;height:24px;border-radius:50%;background:var(--gold);color:var(--navy);align-items:center;justify-content:center;margin-right:6px}
.offer{border-left:4px solid var(--gold);padding:2px 0 2px 14px;margin-bottom:14px}
.dl{list-style:none;padding:0;margin:8px 0}.dl li{padding:7px 0;border-bottom:1px solid rgba(0,0,0,.08)}.dl a{font-weight:700}.dl .muted{display:block;font-size:.88em}.dl a.es{font-weight:600;font-size:.82em;margin-left:8px;padding:1px 8px;border:1px solid currentColor;border-radius:10px;white-space:nowrap}
.story p{font-style:italic}.story .sig{font-style:normal;font-weight:700;margin:0}
.book img{display:block;width:100%;height:auto;margin-top:14px;border-radius:4px;box-shadow:0 4px 12px rgba(0,0,0,.25)}
.offer p{margin:0}
.audios{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin-bottom:1.6rem}
.audio{background:var(--card);border:1px solid var(--line);border-left:4px solid var(--sage);border-radius:10px;padding:12px 14px}
.audio b{display:block;font-family:var(--sans);color:var(--navy);margin-bottom:2px}
.audio .desc{font-size:.9rem;color:var(--muted);margin:0 0 8px}
.audio audio{width:100%}
.givegrid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.form label{display:block;font-size:.9rem;font-weight:600;margin:0 0 4px;color:var(--navy)}
.form input,.form select,.form textarea{width:100%;font:16px/1.4 var(--sans);padding:10px 12px;border:1.5px solid var(--line);border-radius:8px;background:#fff;margin-bottom:12px}
.form textarea{min-height:90px}
.row2{display:grid;grid-template-columns:1fr 1fr;gap:0 14px}
.note{font-size:.85rem;color:#5c4a00;background:#fff1a8;border-radius:8px;padding:6px 10px}
.cta-band{background:var(--navy);color:#fff;text-align:center;padding:48px 0}
.cta-band h2{color:#fff}
.cta-band p{color:#ffffff;max-width:620px;margin:0 auto 1.3rem}
.cta-band .ref{color:#e9dcc6}
footer{background:#5f0423;color:#ffffff;padding:30px 0 20px;font-size:.88rem}
footer a{color:#ffffff}footer b{color:#fff}
.fgrid{display:grid;grid-template-columns:2fr 1fr 1.3fr;gap:20px}
footer .ref{color:#e9dcc6}
@media (max-width:820px){
 .hero.split{padding:0 0 40px;text-align:center}
 .hero.split .wrap{grid-template-columns:1fr;gap:22px;padding:0}
 .hero.split .hero-img{order:0}
 .hero.split .hero-img img{border-radius:0;box-shadow:none}
 .hero.split .hero-text{padding:0 20px}
 .hero .verses{text-align:left}
 .personas,.vgrid,.givegrid{grid-template-columns:1fr 1fr}.two{grid-template-columns:1fr}.path{grid-template-columns:1fr 1fr}.fgrid{grid-template-columns:1fr}
 ol.strip{grid-template-columns:1fr;gap:6px} ol.strip li{display:flex;align-items:center;gap:12px;text-align:left;padding:10px 12px} ol.strip li::before{margin:0;flex:none} ol.strip li b{display:inline;margin:0 6px 0 0}
}
@media (max-width:560px){body{font-size:17px}.personas,.vgrid,.givegrid,.audios,.row2,.grid2{grid-template-columns:1fr}nav a{font-size:.86rem}.stepcard{grid-template-columns:1fr}.path{grid-template-columns:1fr}.hero .btn.ghost,.cta-band .btn.ghost{margin:10px 0 0 0}}
.plist{border:0;padding:0;margin:4px 0 12px}
.plist legend{font-family:var(--sans);font-weight:700;color:var(--navy);font-size:1.05rem;margin-bottom:6px;padding:0}
.plist .pray{background:#fff;border-left:3px solid var(--gold);padding:8px 12px;border-radius:6px}
.pgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:8px;margin:10px 0 14px;align-items:start}
.pg{background:#fff;border:1px solid var(--line);border-radius:8px;padding:6px 10px}
.ph{display:flex;align-items:center;gap:8px}
.form .plist label.ck{display:flex;align-items:flex-start;gap:8px;font-weight:400;color:inherit;margin:0;padding:4px 0;font-size:.93rem;line-height:1.3;cursor:pointer}
.form .plist label.gh{font-weight:700;color:var(--navy);flex:1}
.form .plist input[type=checkbox]{width:18px;height:18px;margin:1px 0 0;flex:none;accent-color:var(--navy)}
.pm{font:600 .78rem var(--sans);background:none;border:1px solid var(--line);border-radius:999px;padding:2px 10px;color:var(--navy);cursor:pointer;white-space:nowrap}
.pi{border-top:1px solid var(--line);margin-top:6px;padding:4px 0 2px 26px}
.pi .gl,.plist .gh .gl{font-weight:400;color:#6b6157;font-size:.85em}
.form .plist label.ot{font-size:.85rem;margin-top:8px}
.form .plist .pi input.pt{margin-bottom:6px}
.stepcard.next .n{background:var(--gold);color:var(--navy)}
'''

if COMBINED:
    HOME = HOME2
    CSS = CSS2
    LOGO = '<img src="brand/dove-badge-96.png" width="40" height="40" alt="">'


page("index.html", "Deliverance Ministries · Freedom and healing in Jesus Christ", "Free deliverance and healing ministry in Oklahoma City and by phone, Zoom or FaceTime.", HOME, "index.html")
page("get-help.html", "Get help · Deliverance Ministries", "Free, personal ministry in person in Oklahoma City or from anywhere.", GETHELP, "get-help.html")
page("help-nearby.html", "Monday nights · Deliverance Ministries", "Free one-on-one ministry every Monday night in Oklahoma City.", NEARBY, "get-help.html")
page("help-anywhere.html", "Help from anywhere · Deliverance Ministries", "A free step-by-step guide at home, then ministry by phone, Zoom or FaceTime.", ANYWHERE, "get-help.html")
page("children.html", "Help for children · Deliverance Ministries", "How ministry for children works and how to request an appointment.", CHILDREN, "get-help.html")
page("learn.html", "Learn to minister · Deliverance Ministries", "Free training videos and handouts for believers who want to minister.", LEARN, "learn.html")
page("churches.html", "For churches · Deliverance Ministries", "Invite a ministry team to teach, minister and train.", CHURCHES, "churches.html")
page("testimonies.html", "Testimonies · Deliverance Ministries", "People share what Jesus has done.", TESTIMONIES, "testimonies.html")
page("give.html", "Give · Deliverance Ministries", "Support free deliverance and healing ministry.", GIVE, "give.html")
page("about.html", "About · Deliverance Ministries", "The enduring ministry of Jesus Christ.", ABOUT, "about.html")
page("thanks.html", "Thank you · Deliverance Ministries", "Your message was sent.", '''
<section class="page-hero"><div class="wrap">
<h1>Thank you</h1>
<p>Your message was sent. Someone from the ministry will get back to you soon.</p>
</div></section>
<section><div class="wrap narrow">
<p>“Yahweh is near to those who have a broken heart, and saves those who have a crushed spirit.” <span class="ref">Psalm 34:18</span></p>
<p><a class="btn" href="index.html">Back to the home page</a></p>
</div></section>
''', "")
page("contact.html", "Contact · Deliverance Ministries", "Contact Deliverance Ministries.", CONTACT, "contact.html")
(OUT/"style.css").write_text(CSS)
print("built", sorted(p.name for p in OUT.iterdir()))
