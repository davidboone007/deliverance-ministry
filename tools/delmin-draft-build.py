# Builds the delmin.org revamp draft into the healing.place repo at /delmin.org-draft/.
# Edit the page bodies here, then run from the repo root: python3 tools/delmin-draft-build.py
import pathlib, sys, html as H
OUT = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent.parent / "delmin.org-draft"
OUT.mkdir(parents=True, exist_ok=True)
SITE = "Deliverance Ministries"
OLD = "https://delmin.org"          # current site; media still lives there until it is moved
UP = OLD + "/wp-content/uploads/2017/09/"

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
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="style.css">
</head>
<body>
<div class="draftbar">Draft preview of a new delmin.org. Not the live site. Forms don't send yet, and <span class="tbc">highlighted</span> facts are still being confirmed.</div>
<header class="top"><div class="wrap">
<a class="brand" href="index.html">{LOGO}<span>{SITE}</span></a>
<nav>{nav}</nav>
</div></header>
<main>
{body}
</main>
<footer><div class="wrap">
<div class="fgrid">
<div><p><b>{SITE}, Inc.</b> {tbc("legal name")}<br>Oklahoma City, Oklahoma<br>Serving since 1984</p>
<p>All ministry is free of charge. “Freely you received, so freely give.” <span class="ref">Matthew 10:8</span></p></div>
<div><p><a href="about.html">About the ministry</a><br><a href="contact.html">Contact us</a><br><a href="get-help.html">Get help</a><br><a href="give.html">Give</a></p></div>
<div><p>Phone (405) 842-5509<br>Mail: 2828 NW 57th, Ste. 305<br>Oklahoma City, OK 73112</p></div>
</div>
<p class="small">Scripture quotations are from the World English Bible (public domain).</p>
</div></footer>
</body>
</html>
'''
    (OUT/fname).write_text(doc)

def form(title, fields, button="Send request"):
    return f'''<form class="card form" onsubmit="return false">
<h3>{title}</h3>
{fields}
<p class="note">Draft preview: this form doesn't send yet.</p>
<div><button class="btn" type="button" disabled>{button}</button></div>
</form>'''

NAME_EMAIL = '''<div class="row2">
<div><label>Your name</label><input type="text" autocomplete="name"></div>
<div><label>Email</label><input type="email" autocomplete="email"></div>
</div>
<div class="row2">
<div><label>Phone</label><input type="tel" autocomplete="tel"></div>
<div><label>City and state</label><input type="text"></div>
</div>'''

def yt(vid, title, length=""):
    meta = f'<span class="len">{length}</span>' if length else ''
    return f'''<figure class="video"><div class="frame"><iframe loading="lazy" src="https://www.youtube-nocookie.com/embed/{vid}" title="{H.escape(title)}" allow="encrypted-media; picture-in-picture" allowfullscreen></iframe></div><figcaption>{title} {meta}</figcaption></figure>'''

ICON = {
 "near": '<svg viewBox="0 0 48 48"><path d="M24 44s14-13 14-24a14 14 0 0 0-28 0c0 11 14 24 14 24z" fill="#17394a"/><circle cx="24" cy="20" r="5.5" fill="#fff"/></svg>',
 "far": '<svg viewBox="0 0 48 48"><rect x="13" y="5" width="22" height="38" rx="4" fill="#17394a"/><rect x="16" y="10" width="16" height="25" rx="1.5" fill="#fff"/><circle cx="24" cy="39" r="1.8" fill="#fff"/><path d="M20 19l4 3-4 3z" fill="#c08a2b"/></svg>',
 "child": '<svg viewBox="0 0 48 48"><circle cx="17" cy="11" r="6" fill="#17394a"/><path d="M7 44V27a10 10 0 0 1 20 0v17z" fill="#17394a"/><circle cx="34" cy="21" r="4.5" fill="#c08a2b"/><path d="M27 44V33a7 7 0 0 1 14 0v11z" fill="#c08a2b"/></svg>',
 "learn": '<svg viewBox="0 0 48 48"><path d="M6 10c7-2 13-1 18 3 5-4 11-5 18-3v28c-7-2-13-1-18 3-5-4-11-5-18-3z" fill="#17394a"/><path d="M24 13v28" stroke="#fff" stroke-width="2"/></svg>',
 "church": '<svg viewBox="0 0 48 48"><path d="M24 4v10M20 8h8" stroke="#17394a" stroke-width="3" stroke-linecap="round"/><path d="M10 44V26l14-11 14 11v18z" fill="#17394a"/><path d="M20 44v-9a4 4 0 0 1 8 0v9z" fill="#c08a2b"/></svg>',
 "give": '<svg viewBox="0 0 48 48"><path d="M24 42S6 31 6 18a9 9 0 0 1 18-3 9 9 0 0 1 18 3c0 13-18 24-18 24z" fill="#c08a2b"/></svg>',
}

def persona(icon, href, title, text, go):
    return f'<a class="persona" href="{href}">{ICON[icon]}<h3>{title}</h3><p>{text}</p><span class="go">{go} →</span></a>'

PERSONAS = "".join([
 persona("near","help-nearby.html","I need help, and I'm near Oklahoma City","Come to a Monday night meeting for free, one-on-one ministry.","Monday nights"),
 persona("far","help-anywhere.html","I need help, but I'm far away","Start a step-by-step guide at home, then meet a minister by phone, Zoom or FaceTime.","Help from anywhere"),
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
<li><b>7:30 pm</b> Personal ministry until about {tbc("10:30 pm")}</li>
</ol>
<p>9201 N. Rockwell, Oklahoma City, OK 73132<br><span class="muted">West side of Rockwell, between NW Expressway and Britton Rd.</span></p>
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
{persona("near","help-nearby.html","Near Oklahoma City","Come to a Monday night meeting.","Monday nights")}
{persona("far","help-anywhere.html","Anywhere else","A guide at home, then phone, Zoom or FaceTime.","Help from anywhere")}
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
<p>Free, one-on-one ministry with trained ministers, every Monday except major holidays {tbc("which ones?")}.</p>
</div></section>
<section><div class="wrap two">
<div>
<h2>Your evening</h2>
<ol class="timeline">
<li><b>5:30 pm</b> Introduction: Jesus' works today, how evil spirits gain access, your authority in Christ, and staying free.</li>
<li><b>6:30 pm</b> Door-closing prayer together. <span class="pill">required before personal ministry</span></li>
<li><b>7:30 pm</b> Personal ministry with a small team, until about {tbc("10:30 pm")}.</li>
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
{form("Reserve a Monday", NAME_EMAIL + '<div><label>Which Monday?</label><input type="date"></div><div><label>Anything we should know? (optional)</label><textarea></textarea></div>', "Reserve")}
<div class="card soft"><h3>Topics we often see</h3><p class="muted">Including but not limited to:</p>
<p>fear and anxiety · depression · addictions · eating disorders · sickness and infirmity · witchcraft and the occult · multiple personalities · troubled homes · emotional wounds</p></div>
</div>
</div></section>
'''

# ---------------- ANYWHERE ----------------
ANYWHERE = f'''
<section class="page-hero"><div class="wrap">
<h1>Help from anywhere</h1>
<p>Can't come on a Monday? Prepare at home with this guide, then meet a trained minister by phone, Zoom or FaceTime. It's free. Steps 1 to 4 take about 3 to 4 hours, and you can pause between them.</p>
<p class="small">Currently offered in the USA {tbc("still USA only?")}.</p>
</div></section>
<section><div class="wrap">
<div class="progress"><span>1 Problem list</span><span>2 Watch</span><span>3 Close the doors</span><span>4 Request a minister</span><span>5 Deliverance</span><span>6 Holy Spirit</span></div>

<div class="stepcard"><div class="n">1</div><div><h3>Circle what applies</h3><p>Print the <a href="{UP}problem-list.pdf">Problem List</a> and circle anything that applies to you. Keep it handy for steps 4 and 5.</p></div></div>
<div class="stepcard"><div class="n">2</div><div><h3>Learn how freedom and healing work</h3>{yt("SiOOB29SQLI","What is deliverance ministry?","1 hr 10 min")}</div></div>
<div class="stepcard"><div class="n">3</div><div><h3>Pray the door-closing prayer <span class="pill">required</span></h3><p>Print the <a href="{UP}brown-handout-4-11.pdf">door-closing prayer handout</a> and pray it aloud as the video leads you. The video also covers how to stay free.</p>{yt("9CH5Lc2y9bQ","The door-closing prayer","31 min")}</div></div>
<div class="stepcard"><div class="n">4</div><div><h3>Request a minister</h3><p>Ask for a free session with a trained minister by phone, Zoom or FaceTime.</p>
{form("Request a session", NAME_EMAIL + '<div><label>How would you like to meet?</label><select><option>Phone call</option><option>Zoom</option><option>FaceTime</option></select></div><div><label>I have finished steps 1 to 3</label><select><option>Yes</option><option>Not yet</option></select></div><div><label>Problems you circled (or attach later)</label><textarea></textarea></div>', "Request a session")}</div></div>
<div class="stepcard"><div class="n">5</div><div><h3>Individual or group deliverance</h3><p>Only after steps 1 to 3. Have your Problem List ready and pause the video whenever you need to.</p>{yt("UJSWP5yNdhY","Individual or group deliverance","1 hr 52 min")}</div></div>
<div class="stepcard"><div class="n">6</div><div><h3>Be filled with the Holy Spirit</h3><p><a href="{UP}the-Baptism-of-the-Holy-Spirit-1.pdf">Handout</a> for this video.</p>{yt("vFJNON4Ld20","The baptism of the Holy Spirit","10 min")}</div></div>
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
<li><b>Request an appointment</b> for your child, ages {tbc("14 and younger")}, within a few weeks of your own ministry {tbc("timing?")}.</li>
<li><b>Minister together.</b> A parent stays with their child throughout.</li>
</ol>
<p class="muted">There is no childcare on Monday nights, so please don't bring children to the general meeting.</p>
<h2>Learn more first</h2>
{yt("sIxPRqK1f8M","Ministering to children")}
</div>
<div>
{form("Request an appointment for your child", NAME_EMAIL + '<div class="row2"><div><label>Child\'s age</label><input type="number" min="0" max="17"></div><div><label>When did you receive ministry?</label><input type="date"></div></div><div><label>Anything we should know? (optional)</label><textarea></textarea></div>', "Request appointment")}
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
<p>Prayers, renunciations, problem lists (including Spanish), and the full training sets on CD and DVD are being updated and converted to free downloads.</p>
<p class="muted">Coming soon {tbc("being converted")}</p></div>
<div class="card soft"><h3>The book</h3>
<p><i>Doing the Supernatural Works of Jesus</i>, the ministry's training manual.</p>
<p><a class="btn ghost" href="#">Get the book {tbc("Amazon link?")}</a></p></div>
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
<p>{cnt} people share, in their own voices, what Jesus has done. Free to listen and share. Downloads coming soon.</p>
</div></section>
<section><div class="wrap">
<p class="muted small">Titles were tidied for this draft, and three duplicate recordings were removed.</p>
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
<div class="card"><h3>Give online</h3><p>One-time or monthly, by card or PayPal.</p><a class="btn" href="{OLD}/donate/">Give online</a><p class="small muted">Opens the current donation page for now.</p></div>
<div class="card"><h3>Give by check</h3><p>Payable to Deliverance Ministries, Inc.<br>2828 NW 57th, Ste. 305<br>Oklahoma City, OK 73112</p></div>
<div class="card"><h3>Where it goes</h3><ul class="check"><li>Free Monday night ministry</li><li>Free phone, Zoom and FaceTime sessions</li><li>Free training and downloads</li><li>Visits to churches and groups</li></ul></div>
</div>
<p class="center muted">“Let each man give according as he has determined in his heart, not grudgingly or under compulsion, for God loves a cheerful giver.” <span class="ref">2 Corinthians 9:7</span></p>
<p class="center small muted">Tax-deductible status {tbc("confirm 501(c)(3) wording")}</p>
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
<p><b>Email</b><br>{tbc("ministry address")}</p>
<p><b>Mail</b><br>Deliverance Ministries, Inc.<br>2828 NW 57th, Ste. 305<br>Oklahoma City, OK 73112</p>
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

FAV = LOGO.replace(' aria-hidden="true"', ' xmlns="http://www.w3.org/2000/svg"')

page("index.html", "Deliverance Ministries · Freedom and healing in Jesus Christ", "Free deliverance and healing ministry in Oklahoma City and by phone, Zoom or FaceTime.", HOME, "index.html")
page("get-help.html", "Get help · Deliverance Ministries", "Free, personal ministry near Oklahoma City or from anywhere.", GETHELP, "get-help.html")
page("help-nearby.html", "Monday nights · Deliverance Ministries", "Free one-on-one ministry every Monday night in Oklahoma City.", NEARBY, "get-help.html")
page("help-anywhere.html", "Help from anywhere · Deliverance Ministries", "A free step-by-step guide at home, then ministry by phone, Zoom or FaceTime.", ANYWHERE, "get-help.html")
page("children.html", "Help for children · Deliverance Ministries", "How ministry for children works and how to request an appointment.", CHILDREN, "get-help.html")
page("learn.html", "Learn to minister · Deliverance Ministries", "Free training videos and handouts for believers who want to minister.", LEARN, "learn.html")
page("churches.html", "For churches · Deliverance Ministries", "Invite a ministry team to teach, minister and train.", CHURCHES, "churches.html")
page("testimonies.html", "Testimonies · Deliverance Ministries", "People share what Jesus has done.", TESTIMONIES, "testimonies.html")
page("give.html", "Give · Deliverance Ministries", "Support free deliverance and healing ministry.", GIVE, "give.html")
page("about.html", "About · Deliverance Ministries", "The enduring ministry of Jesus Christ.", ABOUT, "about.html")
page("contact.html", "Contact · Deliverance Ministries", "Contact Deliverance Ministries.", CONTACT, "contact.html")
(OUT/"style.css").write_text(CSS)
(OUT/"favicon.svg").write_text(FAV)
print("built", sorted(p.name for p in OUT.iterdir()))
