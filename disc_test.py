# This is the test file for the discord bot. 
# I tried using dpytest for testing but couldn't
# get it to work so I'm using pytest to test the helper
# functions which do all of the work

import discobot_helper

def test_get_sets():
    # This is the normal test, just to check good enquiries work
    assert discobot_helper.get_sets("/sets Hippowdon SS") == """```Hippowdon @ Leftovers
Ability: Sand Stream
EVs: 252 HP / 8 Atk / 248 SpD
Careful Nature
- Earthquake
- Slack Off
- Stealth Rock
- Toxic

The set(s) for Hippowdon are from within the OU tier. For sets from a specific tier, type the tier at the end```"""

    # Small checks to ensure the generation and tier is not required
    assert discobot_helper.get_sets("/sets Hippowdon SS") == discobot_helper.get_sets("/sets Hippowdon")

    assert discobot_helper.get_sets("/sets Hippowdon") == discobot_helper.get_sets("/sets Hippowdon SS OU")

    # More than 3 enquiries offered
    assert discobot_helper.get_sets("/sets Hippowdon SS SM OU") == """```Hippowdon @ Leftovers
Ability: Sand Stream
EVs: 252 HP / 8 Atk / 248 SpD
Careful Nature
- Earthquake
- Slack Off
- Stealth Rock
- Toxic

The set(s) for Hippowdon are from within the OU tier from your specified (or SS) generation, since there was some error with your specified tier, hence the default sets are shown. For sets from a specific tier, type the tier at the end```"""

    # Incorrect Pokemon, Generation or Tier test or the Pokemon doesnt have an analysis for the given generation and tier
    # Ideally they should be different but I haven't implemented that fully
    assert discobot_helper.get_sets("/sets Hippodown SS") == "```The Pokemon doesn't have an analysis in said generation and tier```"

    # A Pokemon which was Dexit'd
    assert discobot_helper.get_sets("/sets Eelektross") == "```The Pokemon doesn't have an analysis in said generation and tier```"

    # Finally, we also check whether adding to the file works or not. Rightfully, it will only work once, change Tiers.txt to test this
    # some = open("Tiers.txt")
    # old_str = some.read()
    # discobot_helper.get_sets("/sets Blissey Uber")
    # some.close()
    # othersome = open("Tiers.txt")
    # new_str = othersome.read()
    # assert old_str != new_str
    # othersome.close()

    # Also have to check for tiers with more than 1 word
    assert discobot_helper.get_sets("/sets Hydreigon Almost Any Ability") == """Hydreigon @ Choice Scarf
Ability: Regenerator
EVs: 252 SpA / 4 SpD / 252 Spe
Timid Nature
- Draco Meteor
- Dark Pulse
- U-turn
- Fire Blast

The set(s) for Hydreigon are from within the Almost Any Ability tier. For sets from a specific tier, type the tier at the end"""

    assert discobot_helper.get_sets("/sets Hydreigon Almost Any Ability") == discobot_helper.get_sets("/sets Hydreigon SS Almost Any Ability")

def test_get_tiers():
    pass