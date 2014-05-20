#Bored waiting for the proxy to come back up

import random
from time import sleep
from math import sqrt

class item:
    def __init__(self):
        self.name = "Nothing"
        self.quality = -1
        self.cost = 0
        self.power = 0
        self.ilevel = 0

    def getQualityAbbr(self):
        if self.quality == -1:
            return " "
        if self.quality == 0:
            return "d"
        if self.quality == 1:
            return "b"
        if self.quality == 2:
            return "c"
        if self.quality == 3:
            return "u"
        if self.quality == 4:
            return "R"
        if self.quality == 5:
            return "L"
        return "G"

class bodyPart:
    def __init__(self):
        self.name = "Unknown"
        self.size = 0
        self.is_weapon = False
        self.multiplier = 1.00
        self.armor_list = []
        self.armor = item()

class mod:
    def __init__(self):
        self.name = "Nothingness"
        self.power_mod = 0
        self.mlevel = 0

class spell:
    def __init__(self):
        self.name = "Nothing"
        self.mp_cost = 0
        self.power = 0

class entity:
    def __init__(self):
        self.name = "Noone"
        self.species = "Unknown"
        self.body_parts = []
        self.gold = 0
        self.hp_max = 0
        self.hp_cur = 0
        self.mp_max = 0
        self.mp_cur = 0
        self.str = 0
        self.exp = 0
        self.level = 0
        self.crit = 0.05
        self.to_hit = 0.95
        self.dodge = 0.05
        self.parry = 0.01
        self.speed = 5
        self.cast_freq = 0.15
        self.weapon = item()

def get_random_place(placeList):
    buffer = ""

    if int(99*random.random()) > 33:
        buffer = buffer + random.choice(places_prefixes) + " "

    buffer = buffer + random.choice(placeList) + " "

    if int(99*random.random()) > 15:
        buffer = buffer + random.choice(places_suffixes) + " "

    buffer = buffer.rstrip().title()
    return buffer

def get_random_mod(modList, mLevel):
    a_mod = mod()
    a_mod.mlevel = mLevel + 1 + int(3*random.random())
    a_mod.name = random.choice(modList)
    a_mod.power_mod = a_mod.mlevel + int(a_mod.mlevel * (0.25 - (random.random()/2.0)))

    return a_mod

def get_random_item(typeList, iLevel, isWeapon):
    buffer = ""
    cost = 50
    power = 0
    random_item = item()

    quality_chance = random.random()
    second_chance = random.random()

    #The base item
    a_mod = get_random_mod(typeList, (iLevel+10))
    buffer = buffer + a_mod.name
    power = power + a_mod.power_mod
    cost = cost + (power * power)
    random_item.ilevel = random_item.ilevel + a_mod.mlevel

    if quality_chance > 0.500:
        #common item
        if second_chance > 0.800:
            #broken
            random_item.quality = 1
        elif second_chance > 0.600:
            #very broken
            random_item.quality = 0
        else:
            #standard item
            random_item.quality = 2
    elif quality_chance > 0.250:
        #uncommon
        random_item.quality = 3
    elif quality_chance > 0.050:
        #rare
        random_item.quality = 4
    elif quality_chance > 0.005:
        #heroic
        random_item.quality = 5
    else:
        #godlike
        random_item.quality = 6

    if random_item.quality <= 1:
        #add a garbage prefix
        a_mod = get_random_mod(garbage_prefixes, iLevel)
        buffer = a_mod.name + " " + buffer
        power = int((power + a_mod.power_mod) * 0.50)
        cost = int(cost * 0.25)

        if random_item.quality == 0:
            #add a garbage suffix
            a_mod = get_random_mod(garbage_suffixes, iLevel)
            buffer = buffer + " " + a_mod.name
            power = int((power + a_mod.power_mod) * 0.50)
            cost = int(cost * 0.25)

    if random_item.quality >= 3:
        #add a quality prefix
        a_mod = get_random_mod(quality_prefixes, iLevel)
        buffer = a_mod.name + " " + buffer
        power = power + a_mod.power_mod
        cost = cost + (power * power)

    if random_item.quality >= 5:
        #add a descriptive prefix
        if isWeapon:
            a_mod = get_random_mod(weapons_prefixes, iLevel)
        else:
            a_mod = get_random_mod(armors_prefixes, iLevel)
        buffer = a_mod.name + " " + buffer
        power = power + a_mod.power_mod
        cost = cost + (power * power)

    if random_item.quality >= 6:
        #add a descriptive suffix
        if isWeapon:
            a_mod = get_random_mod(weapons_suffixes, iLevel)
        else:
            a_mod = get_random_mod(armors_suffixes, iLevel)
        buffer = buffer + " " + a_mod.name
        power = power + a_mod.power_mod
        cost = cost + (power * power)

    if random_item.quality >= 4:
        #add a quality suffix
        a_mod = get_random_mod(quality_suffixes, iLevel)
        buffer = buffer + " " + a_mod.name
        power = power + a_mod.power_mod
        cost = cost + (power * power)

    random_item.name = "[" + buffer.title().rstrip() + "]"
    random_item.cost = cost
    random_item.power = power

    return random_item

def get_random_spell(spellList):
    buffer = ""
    cost = 0
    power = 0
    random_spell = spell()

    if int(99*random.random()) > 60:
        buffer = buffer + random.choice(spells_prefixes) + " "
        cost = cost + int(4000*random.random())
        power = power + int(sqrt(cost)) + 1

    buffer = buffer + random.choice(spellList) + " "
    cost = cost + int(250*random.random())
    power = power + int(sqrt(cost)) + 1

    random_spell.name = "{" + buffer.title().rstrip() + "}"
    random_spell.mp_cost = cost
    random_spell.power = power

    return random_spell

def choose_spell(spellList, minimum=1, maximum=1):
    while(1):
        a_spell = get_random_spell(spellList)
        if a_spell.mp_cost >= minimum and a_spell.mp_cost <= maximum:
            return a_spell

def shop_for_item(typeList, minimum=1, budget=1, powerReq=1, iLevel=1, isWeapon=False):
    checked_items = 0
    while(checked_items < 1000):
        random_item = get_random_item(typeList, iLevel, isWeapon)
        if random_item.cost >= minimum and random_item.cost <= budget and random_item.power >= powerReq:
            return random_item
        checked_items = checked_items + 1
    return item()

def create_monster(monsterList, minLevel=0, maxLevel=99):
    buffer = ""
    gold = 0
    str = 0
    random_monster = entity()

    if minLevel < 1:
        minLevel = 1

    if int(99*random.random()) < 33:
        buffer = buffer + random.choice(monsters_prefixes) + " "
        gold = gold + int(25*random.random())
        str = str + int(5*random.random())

    buffer = buffer + random.choice(monsterList) + " "
    gold = gold + int(50*random.random())
    str = str + int(3*random.random())

    #monsters are occassionally rich
    if random.random() < 0.05:
        gold = gold * 10

    random_monster.name = buffer.rstrip()
    random_monster.level = minLevel + int((maxLevel-minLevel)*random.random())
    random_monster.str = int(str * ((1 + random.random()) * (random_monster.level * 0.6)))
    random_monster.hp_max = 70 + int(int(6*random.random()) * (random_monster.level * 1.1))
    random_monster.mp_max = 8 + int(int(4*random.random()) * (random_monster.level * 0.8))
    random_monster.gold = int(gold * (1 + (random_monster.level * 0.4)))

    #determine fighting style
    if random.random() > 0.50:
        #physical
        speed_ratio = 0.50 + random.random()
        random_monster.speed = int(random_monster.speed * speed_ratio)
        random_monster.str = int(random_monster.str / speed_ratio)
        random_monster.cast_freq = 0.15
        random_monster.mp_max = int(random_monster.mp_max * 0.25)
    else:
        #magical
        speed_ratio = 0.35 + random.random()
        random_monster.speed = int(random_monster.speed * speed_ratio)
        random_monster.hp_max = int(random_monster.hp_max * 0.80)
        random_monster.mp_max = int(1.5 * (random_monster.mp_max / speed_ratio))
        random_monster.cast_freq = 0.85
        random_monster.str = int(random_monster.str * 0.5)

    random_monster.hp_cur = random_monster.hp_max
    random_monster.mp_cur = random_monster.mp_max

    return random_monster

#Where to load our word lists
places_towns_path = "./entities/places_towns.txt"
places_adventure_path = "./entities/places_adventure.txt"
weapons_path = "./entities/weapons.txt"
armors_path = "./entities/armors.txt"
helmets_path = "./entities/helmets.txt"
monsters_path = "./entities/monsters.txt"
gloves_path = "./entities/gloves.txt"
pants_path = "./entities/pants.txt"
boots_path = "./entities/boots.txt"
weapons_prefixes_path = "./entities/weapons_prefixes.txt"
armors_prefixes_path = "./entities/armors_prefixes.txt"
monsters_prefixes_path = "./entities/monsters_prefixes.txt"
places_prefixes_path = "./entities/places_prefixes.txt"
spells_prefixes_path = "./entities/spells_prefixes.txt"
weapons_suffixes_path = "./entities/weapons_suffixes.txt"
armors_suffixes_path = "./entities/armors_suffixes.txt"
places_suffixes_path = "./entities/places_suffixes.txt"
quality_prefixes_path = "./entities/quality_prefixes.txt"
quality_suffixes_path = "./entities/quality_suffixes.txt"
garbage_prefixes_path = "./entities/garbage_prefixes.txt"
garbage_suffixes_path = "./entities/garbage_suffixes.txt"
spells_attack_path = "./entities/spells_attack.txt"

#Here are various word lists
places_towns = []
with open(places_towns_path, "r") as f:
    for line in f:
        places_towns.append(line.rstrip())

places_adventure = []
with open(places_adventure_path, "r") as f:
    for line in f:
        places_adventure.append(line.rstrip())
    
weapons = []
with open(weapons_path, "r") as f:
    for line in f:
        weapons.append(line.rstrip())
        
armors = []
with open(armors_path, "r") as f:
    for line in f:
        armors.append(line.rstrip())

helmets = []
with open(helmets_path, "r") as f:
    for line in f:
        helmets.append(line.rstrip())

monsters = []
with open(monsters_path, "r") as f:
    for line in f:
        monsters.append(line.rstrip())

gloves = []
with open(gloves_path, "r") as f:
    for line in f:
        gloves.append(line.rstrip())

pants = []
with open(pants_path, "r") as f:
    for line in f:
        pants.append(line.rstrip())
        
boots = []
with open(boots_path, "r") as f:
    for line in f:
        boots.append(line.rstrip())

weapons_prefixes = []
with open(weapons_prefixes_path, "r") as f:
    for line in f:
        weapons_prefixes.append(line.rstrip())

armors_prefixes = []
with open(armors_prefixes_path, "r") as f:
    for line in f:
        armors_prefixes.append(line.rstrip())

monsters_prefixes = []
with open(monsters_prefixes_path, "r") as f:
    for line in f:
        monsters_prefixes.append(line.rstrip())

places_prefixes = []
with open(places_prefixes_path, "r") as f:
    for line in f:
        places_prefixes.append(line.rstrip())


spells_prefixes = []
with open(spells_prefixes_path, "r") as f:
    for line in f:
       spells_prefixes.append(line.rstrip())

armors_suffixes = []
with open(armors_suffixes_path, "r") as f:
    for line in f:
       armors_suffixes.append(line.rstrip())

weapons_suffixes = []
with open(weapons_suffixes_path, "r") as f:
    for line in f:
       weapons_suffixes.append(line.rstrip())
       
places_suffixes = []
with open(places_suffixes_path, "r") as f:
    for line in f:
       places_suffixes.append(line.rstrip())

quality_prefixes = []
with open(quality_prefixes_path, "r") as f:
    for line in f:
       quality_prefixes.append(line.rstrip())

quality_suffixes = []
with open(quality_suffixes_path, "r") as f:
    for line in f:
      quality_suffixes.append(line.rstrip())

garbage_prefixes = []
with open(garbage_prefixes_path, "r") as f:
    for line in f:
       garbage_prefixes.append(line.rstrip())
       
garbage_suffixes = []
with open(garbage_suffixes_path, "r") as f:
    for line in f:
       garbage_suffixes.append(line.rstrip())
       
spells_attack = []
with open(spells_attack_path, "r") as f:
    for line in f:
       spells_attack.append(line.rstrip())

#Time multiplier
time_mult = 3.00

#Gather some info on the hero
our_hero = entity()

#Add some pieces
temp_piece = bodyPart()
temp_piece.name = "Weapon"
temp_piece.size = 3
temp_piece.is_weapon = True
temp_piece.multiplier = 0.50
temp_piece.armor_list = weapons
our_hero.body_parts.append(temp_piece)
our_hero.weapon = temp_piece.armor

temp_piece = bodyPart()
temp_piece.name = "Head"
temp_piece.size = 6
temp_piece.multiplier = 1.35
temp_piece.armor_list = helmets
our_hero.body_parts.append(temp_piece)

temp_piece = bodyPart()
temp_piece.name = "Body"
temp_piece.size = 24
temp_piece.multiplier = 1.00
temp_piece.armor_list = armors
our_hero.body_parts.append(temp_piece)

temp_piece = bodyPart()
temp_piece.name = "Front Legs"
temp_piece.size = 12
temp_piece.multiplier = 0.85
temp_piece.armor_list = pants
our_hero.body_parts.append(temp_piece)

temp_piece = bodyPart()
temp_piece.name = "Rear Legs"
temp_piece.size = 12
temp_piece.multiplier = 0.85
temp_piece.armor_list = pants
our_hero.body_parts.append(temp_piece)

temp_piece = bodyPart()
temp_piece.name = "Front Hooves"
temp_piece.size = 3
temp_piece.multiplier = 0.90
temp_piece.armor_list = gloves
our_hero.body_parts.append(temp_piece)

temp_piece = bodyPart()
temp_piece.name = "Rear Hooves"
temp_piece.size = 3
temp_piece.multiplier = 0.90
temp_piece.armor_list = boots
our_hero.body_parts.append(temp_piece)

our_hero.name = raw_input("What is your name? ")
our_hero.species = raw_input("What is your species? ")

#Make our town
home_town = get_random_place(places_towns)

#Starting attributes
our_hero.hp_max = 120
our_hero.hp_cur = 120
our_hero.mp_max = 70
our_hero.mp_cur = 70
our_hero.gold = 200
our_hero.level = 1
our_hero.speed = 5
our_hero.exp = 0
our_hero.crit = 0.10
our_hero.to_hit = 0.92
our_hero.dodge = 0.05
our_hero.parry = 0.01

#Begin the quest
print "Brave " + our_hero.name + " of the " + our_hero.species + "s, your journey begins in the " + home_town +  "!"

playing = True

while playing:
    #Ask the player what to do
    ans = raw_input("What shall you do? [adventure/shop/character/quit] ")

    if ans in ["character", "char", "Char", "CHAR", "Character", "CHARACTER", "c", "C"]:
        print our_hero.name + " is a level " + str(our_hero.level) + " " + our_hero.species + " with " + str(our_hero.hp_max) + " hp and " + str(our_hero.mp_max) + " mp"
        print our_hero.name + " is currently wearing:"
        for i in our_hero.body_parts:
            print " " + i.name + "\t" + i.armor.getQualityAbbr() + " " + i.armor.name + " with iLvl " + str(i.armor.ilevel) + " (" + str(i.armor.power) + " power)" + str(i.size)
    elif ans in ["shop", "s", "S", "Shop", "SHOP"]:
        #Go to town to heal and buy items
        print "\nHeading to the " + home_town + " for supplies with " + str(our_hero.gold) + " gold"
        sleep(2/time_mult)

        our_hero.hp_cur = our_hero.hp_max
        our_hero.mp_cur = our_hero.mp_max

        for i in our_hero.body_parts:
            minToSpend = int(our_hero.gold * 0.75)
            if (i.armor.power == 0 or (minToSpend > i.armor.cost and random.random() < 0.50)) and minToSpend > 50:
                potential_item = shop_for_item(i.armor_list, minToSpend, our_hero.gold, i.armor.power-1, our_hero.level, i.is_weapon)
                if potential_item.quality > -1:
                    print "Bought " + potential_item.name + " for " + str(potential_item.cost) + " gold (" + str(potential_item.power) + " power)"
                    i.armor = potential_item
                    if i.is_weapon:
                        our_hero.weapon = potential_item
                    our_hero.gold = our_hero.gold - i.armor.cost
                    sleep(1/time_mult)

        print our_hero.name + " has " + str(our_hero.gold) + " gold left after shopping!\n"
    elif ans in ["adventure", "a", "A", "Adventure", "ADVENTUURE", "grind", "GRIND", "Grind", "g"]:
        #Go out into the wild to fight
        adventuring = True
        print "Adventuring in the " + get_random_place(places_adventure) + "..."

        sleep(3/time_mult)

        while adventuring:
            random_monster = create_monster(monsters, our_hero.level-3, our_hero.level+3)
            estimated_hp = random_monster.hp_max + int(random_monster.hp_max*0.25*(0.5-random.random()))
            estimated_mp = random_monster.mp_max + int(random_monster.mp_max*0.25*(0.5-random.random()))
            estimated_str = random_monster.str + int(random_monster.str*0.25*(0.5-random.random()))
            level_penalty = ((random_monster.level - our_hero.level) * 0.02)
            print "\nEncountered Lv. " + str(random_monster.level) + " " + random_monster.name + " (~" + str(estimated_hp) + " hp/" + str(estimated_mp) + " mp/" + str(estimated_str) + " str)"
            print our_hero.name + " is a level " + str(our_hero.level) + " " + our_hero.species + " with " + str(our_hero.hp_cur) + " hp and " + str(our_hero.mp_cur) + " mp\n"
            ans = raw_input("What shall you do? [fight/run] ")
            if ans in ["fight", "Fight", "FIGHT", "f", "F", "a", "A"]:
                sleep(1/time_mult)
                #prepare the timings
                our_turn = our_hero.speed + 1
                their_turn = random_monster.speed
                while our_hero.hp_cur > 0 and random_monster.hp_cur > 0:
                    #Determine who goes first
                    if our_turn > their_turn:
                        turn = 0
                        their_turn = their_turn + random_monster.speed
                    elif their_turn > our_turn:
                        turn = 1
                        our_turn = our_turn + our_hero.speed
                    else:
                        turn = int(random.random())
                        if turn == 0:
                            their_turn = their_turn + random_monster.speed
                        else:
                            our_turn = our_turn + our_hero.speed

                    if turn == 0:
                        #Do our attack
                        print "\n" + our_hero.name + ": " + str(our_hero.hp_cur) + " hp / " + str(our_hero.mp_cur) + " mp         " + random_monster.name + ": " + str(random_monster.hp_cur) + " hp / " + str(random_monster.mp_cur) + " mp"
                        ans = raw_input("Pick an action [attack/magic] ")
                        if ans in ["magic", "Magic", "MAGIC", "m", "M"]:
                            #Perform a magic attack
                            print our_hero.name + " begins chanting something"
                            sleep(0.75/time_mult)
                            attack_spell = choose_spell(spells_attack,our_hero.mp_cur*0.25,our_hero.mp_cur)
                            damageDealt = int(attack_spell.power * (2.0 + (6.0*random.random())))
                            if random.random() < our_hero.crit:
                                damageDealt = int(damageDealt * 1.75)
                                print our_hero.name + "'s " + attack_spell.name + " critically hits the " + random_monster.name + " for *" + str(damageDealt) + "* damage!"
                            else:
                                print our_hero.name + "'s " + attack_spell.name + " hits the " + random_monster.name + " for " + str(damageDealt) + " damage!"
                            random_monster.hp_cur = random_monster.hp_cur - damageDealt
                            our_hero.mp_cur = our_hero.mp_cur - attack_spell.mp_cost
                        elif ans in ["attack", "Attack", "ATTACK", "a", "A"]:
                            #Perform a physical attack
                            if random.random() > (our_hero.to_hit - level_penalty):
                                print our_hero.name + " misses!"
                            elif random.random() < random_monster.dodge:
                                print "The " + random_monster.name + " dodges!"
                            elif random.random() < random_monster.parry:
                                print "The " + random_monster.name + " parries!"
                            else:
                                #it is a hit
                                damageDealt = int(our_hero.weapon.power + (our_hero.weapon.power * 0.36 * (0.5 - random.random())))
                                if random.random() < our_hero.crit:
                                    damageDealt = int(damageDealt * 2.0)
                                    print our_hero.name + " critically strikes the " + random_monster.name + " for *" + str(damageDealt) + "* damage!"
                                else:
                                    print our_hero.name + " strikes the " + random_monster.name + " for " + str(damageDealt) + " damage!"
                                random_monster.hp_cur = random_monster.hp_cur - damageDealt
                        sleep(1.0/time_mult)

                        #Did we kill it?
                        if random_monster.hp_cur <= 0:
                            break
                    elif turn == 1:
                        #Do the enemy attack
                        if random.random() < random_monster.cast_freq and random_monster.mp_cur > (random_monster.mp_max * 0.25):
                            #Perform a magic attack
                            print "The " + random_monster.name + " begins chanting something"
                            sleep(1.50/time_mult)
                            attack_spell = choose_spell(spells_attack,random_monster.mp_cur*0.25,random_monster.mp_cur)
                            
                            #determine what the enemy is hitting
                            random_part = random.choice([i for part in our_hero.body_parts for i in [part] * part.size ])
                            
                            damageDealt = int((attack_spell.power * (2.0 + (6.0*random.random())))  * random_part.multiplier)
                            if random.random() < our_hero.crit:
                                damageDealt = int(damageDealt * 1.75)
                                print "The " + random_monster.name + "'s " + attack_spell.name + " critically hits " + our_hero.name + "'s " + random_part.name.lower() + " for *" + str(damageDealt) + "* damage!"
                            else:
                                print "The " + random_monster.name + "'s " + attack_spell.name + " hits " + our_hero.name + "'s " + random_part.name.lower() + " for " + str(damageDealt) + " damage!"
                            our_hero.hp_cur = our_hero.hp_cur - damageDealt
                            random_monster.mp_cur = random_monster.mp_cur - attack_spell.mp_cost
                        else:
                            #Physical attack
                            if random.random() > (random_monster.to_hit + level_penalty):
                                print "The " + random_monster.name + " misses!"
                            elif random.random() < our_hero.dodge:
                                print our_hero.name + " dodges!"
                            elif random.random() < our_hero.parry:
                                print our_hero.name + " parries!"
                            else:
                                #it is a hit, so determine what the enemy is hitting
                                random_part = random.choice([i for part in our_hero.body_parts for i in [part] * part.size ])

                                damageDealt = int((random_monster.str + (random_monster.str * 0.36 * (0.5 - random.random()))) * random_part.multiplier)
                                if random.random() < random_monster.crit:
                                    damageDealt = int(damageDealt * 2.0)
                                    print "The " + random_monster.name + " critically strikes " + our_hero.name + "'s " + random_part.name.lower() + " for *" + str(damageDealt) + "* damage!"
                                else:
                                    print "The " + random_monster.name + " strikes " +  our_hero.name + "'s " + random_part.name.lower() + " for " + str(damageDealt) + " damage!"
                                our_hero.hp_cur = our_hero.hp_cur - damageDealt
                        sleep(1.0/time_mult)

                #Are we still alive?
                if our_hero.hp_cur > 0:
                    print "\n" + our_hero.name + " defeated the " + random_monster.name
                    print our_hero.name + " received " + str(random_monster.gold) + " gold"
                    experienceGain = 200 + ((random_monster.level - our_hero.level) * 50)
                    print our_hero.name + " received " + str(experienceGain) + " exp"
                    our_hero.gold = our_hero.gold + random_monster.gold
                    our_hero.exp = our_hero.exp + experienceGain
                    #Did we level up?
                    if our_hero.exp > 1000:
                        our_hero.level = our_hero.level + 1
                        gained_hp = 1 + int(6*random.random())
                        gained_mp = 1 + int(6*random.random())
                        our_hero.hp_max = our_hero.hp_max + gained_hp
                        our_hero.mp_max = our_hero.mp_max + gained_mp
                        our_hero.exp = 0
                        print "\n********************************************"
                        print our_hero.name + " is now level " + str(our_hero.level) + "!"
                        print our_hero.name + " gains " + str(gained_hp) + " hp!"
                        print our_hero.name + " gains " + str(gained_mp) + " mp!"
                        print "********************************************"
                else:
                    #We died!
                    print "\n" + our_hero.name + " has been defeated!"
                    print our_hero.name + " loses " + str(int(our_hero.exp * 0.25)) + " exp and " + str(int(our_hero.gold * 0.10)) + " gold"
                    our_hero.exp = int(our_hero.exp * 0.75)
                    our_hero.gold = int(our_hero.gold * 0.90)
            elif ans in ["run", "Run", "RUN", "r", "R"]:
                print our_hero.name + " has fled!"
                adventuring = False
    if ans in ["quit", "Quit", "QUIT", "q", "Q", "exit", "Exit", "EXIT", "e", "E"]:
        raw_input("Press any key to exit")
        playing = False

