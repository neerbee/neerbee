food_traits = {
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
        'breakfast'
    }

bar_traits = {
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

coffee_traits = {
        # Coffee
        'board_games',
        'frapou',
        'espresso_bar',
        'coffee_on_the_go',
        'work_and_study',
        'big_cups'
    }

hood_traits = {    
        # Hood
        'downtown',
        'busy',
        'underground',
        'suburbs',
        'by_the_sea',
        'posh_hood',
        'calm',
        'touristic',
        'corporate',
    }

space_traits = {
        # Space
        'modern',
        'prive',
        'traditional',
        'spacey',
        'colourful',
        'minimal',
        'retro',
        'concept',
        'table_sharing',
        'house_like',
        'sofas',
        'big_tables',
        'cozy',
        'crowded',
        'great_view',
        'terrace',
        'open_air',
        'garden'
    }

crowd_traits = {
        # Crowd
        'kids',
        'students',
        'females',
        'males',
        'professionals',
        'young_professionals',
        'hipsters',
        'old_people',
        'hippies',
        'indy',
        'posh',
        'couples',
        'celebrities',
        'singles',
        'gay_lesbian',
        'families',
        'artists',
        'musicians'
    }

ambience_traits = {    
        # Ambience
        'noisy',
        'dark',
        'beer_smell',
        'smokey',
        'romantic',
        'candles',
        'sexy',
        'flashy',
        'flirty',
        'bright',
        'clean',
        'party',
        'friendly',
        'family_like',
        'quiet',
        'loud',
        'chillout'
    }

music_traits = {
        # Music
        'mainstream',
        'rock',
        'hip_hop',
        'electronic',
        'house',
        'greek_pop',
        'alternative',
        'latin',
        'jazz',
        'eclectic',
        'atmospheric',
        'disco',
        'oldschool',
        'live',
        'karaoke',
        'goth',
        'metal',
        'heavy_greek',
        'rebetika',
        'funk_soul',
        'loud',
        'soft',
        'radio',
        'no_music',
        'dj_based'
    }

non_service_traits = hood_traits | space_traits | crowd_traits | ambience_traits | music_traits


def get_service_traits(service_type):
    return {
        'Food': food_traits,
        'Bar': bar_traits,
        'Coffee': coffee_traits    
        }.get(service_type, set())

def get_non_service_traits():
    return non_service_traits
    


    
    

    

    

    
