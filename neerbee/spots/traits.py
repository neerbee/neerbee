from mongoengine import *

traits = {
    # Restaurant
    'italian',
    'taverna',
    'mexican',
    'burgers',
    'thai',
    'chinese',
    'french',
    'sushi',
    'asian',
    'tapas',
    'english',
    'modern_greek',
    'chef',
    'traditional_greek',
    'mezedes',
    'cretan',
    'grill_souvlaki',
    'fish',
    'homemade',
    'exotic',
    'vegetarian',
    'beerfood',
    'indian',
    'turkish',
    'molecular',
    'crepes',
    'healthy',
    'big_portions',
    'minimal_food',
    'dirty',
    'sharing',
    'buffet',
    'food_on_the_go',
    'after_hours',
    'brunch',
    'latin',
    'spicy',
    'comforting',
    'steakhouse',
    'breakfast',
    # Bar
    'dance',
    'shots',
    'cocktails',
    'wine',
    'pub',
    'big_club',
    'small',
    'sitting',
    'gigs',
    'clean_drinks',
    'face_control',
    'sit_at_the_bar',
    'hotel_bar',
    'kername',
    'shisha',
    'raki_tsipouro',
    'sports',
    'gay_bar'

    }


class OldTraits(EmbeddedDocument):
    # Bar
    dance = BooleanField()
    shots = BooleanField()
    cocktails = BooleanField()
    wine = BooleanField()
    pub = BooleanField()
    big_club = BooleanField()
    small = BooleanField()
    sitting = BooleanField()
    gigs = BooleanField()
    clean_drinks = BooleanField()
    face_control = BooleanField()
    sit_at_the_bar = BooleanField()
    hotel_bar = BooleanField()
    kername = BooleanField()
    shisha = BooleanField()
    raki_tsipouro = BooleanField()
    sports = BooleanField()
    gay_bar = BooleanField()

    # Coffee
    board_games = BooleanField()
    frapou = BooleanField()
    espresso_bar = BooleanField()
    coffee_on_the_go = BooleanField()
    work_and_study = BooleanField()
    big_cups = BooleanField()

    # Hood
    downtown = BooleanField()
    busy = BooleanField()
    underground = BooleanField()
    suburbs = BooleanField()
    by_the_sea = BooleanField()
    posh_hood = BooleanField()
    calm = BooleanField()
    touristic = BooleanField()
    corporate = BooleanField()

    # Space
    modern = BooleanField()
    prive = BooleanField()
    traditional = BooleanField()
    spacey = BooleanField()
    colourful = BooleanField()
    minimal = BooleanField()
    retro = BooleanField()
    concept = BooleanField()
    table_sharing = BooleanField()
    house_like = BooleanField()
    sofas = BooleanField()
    big_tables = BooleanField()
    cozy = BooleanField()
    crowded = BooleanField()
    great_view = BooleanField()
    terrace = BooleanField()
    open_air = BooleanField()
    garden = BooleanField()

    # Crowd
    kids = BooleanField()
    students = BooleanField()
    females = BooleanField()
    males = BooleanField()
    professionals = BooleanField()
    young_professionals = BooleanField()
    hipsters = BooleanField()
    old_people = BooleanField()
    hippies = BooleanField()
    indy = BooleanField()
    posh = BooleanField()
    couples = BooleanField()
    celebrities = BooleanField()
    singles = BooleanField()
    gay_lesbian = BooleanField()
    families = BooleanField()
    artists = BooleanField()
    musicians = BooleanField()

    # Ambience
    noisy = BooleanField()
    dark = BooleanField()
    beer_smell = BooleanField()
    smokey = BooleanField()
    romantic = BooleanField()
    candles = BooleanField()
    sexy = BooleanField()
    flashy = BooleanField()
    flirty = BooleanField()
    bright = BooleanField()
    clean = BooleanField()
    party = BooleanField()
    friendly = BooleanField()
    family_like = BooleanField()
    quiet = BooleanField()
    loud = BooleanField()
    chillout = BooleanField()

    # Music
    mainstream = BooleanField()
    rock = BooleanField()
    hip_hop = BooleanField()
    electronic = BooleanField()
    house = BooleanField()
    greek_pop = BooleanField()
    alternative = BooleanField()
    latin = BooleanField()
    jazz = BooleanField()
    eclectic = BooleanField()
    atmospheric = BooleanField()
    disco = BooleanField()
    oldschool = BooleanField()
    live = BooleanField()
    karaoke = BooleanField()
    goth = BooleanField()
    metal = BooleanField()
    heavy_greek = BooleanField()
    rebetika = BooleanField()
    funk_soul = BooleanField()
    loud = BooleanField()
    soft = BooleanField()
    radio = BooleanField()
    no_music = BooleanField()
    dj_based = BooleanField()
