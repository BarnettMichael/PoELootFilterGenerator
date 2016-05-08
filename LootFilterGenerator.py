## Path Of Exile Loot Filter Generator Python Script
##
## This is a tool that allows you to easily generate complex Loot Filters 
## quickly, without a lot of typing.
## Data taken from pathofexile.gamepedia.com 
## valid with Path of Exile version 2.1.2 

## DivinationCards
## Gems, Quality highlighted, all displayed -Done
## Jewels, highlighted based on rarity.
## Items based on Rarity, Ilevel and tier. eg rare < 60 shows as chaos, magic <60 only shows if toptier or 5link etc..
## Flasks based on BaseType (already written in other script)
## Recipes: Regal, Chaos, Chromatic, Chisel, Crafting Flasks, Rare rustic sash/chainbelt, Quality white items
    
##Rarity Dependencies, Rare ---> Border depends on 6or5Link/Regal/Chaos/TopTier/Crafting/ilevel Tier, 
##                               Background on 6or5Link/Top tier, Crafting, ilevel tier
##                               FontSize Standard until obsolete then medium.
##                     Magic --> Border Depends on 6or5Link/Tier,
##                               Background on 6or5Link/TopTier/crafting/ilevel tier 
##                               FontSize Standard when top ilevel, medium when 2nd tier, small when obsolete    
##                     Normal--> Border Depends on 6or5Link/Regal/TopTier/Crafting/ilevel tier
##                               Background Depends on 6or5Link/TopTier/Crafting/ilevel tier
##                               FontSize depends on Regal/TopTier&Linked

##Map Fragments needed?

## Done: Gems, Currency, Opening, 5 and 6 linkItems, Jewels, Maps, Uniques, 
##       Regal, Chaos, Chromatic, Chisel(whiteonly), Quality White Items, 
##       6Sockets, Tierbased Sorting, JEWELLERY!, Flasks, Show All MissedEnding 
##       Crafting Flasks Magic and Normal Jewellery and Quivers, Maelstrom Staff work around
## To Do: Good and Bad colours for each Rarity other than unique, then use those (txt color mainly)
##
##       highlight drop only gems
##       top-tier base only shown on white items, high ilvl only? leave magic and rares
##       different ilvl for each basetype, want ilvl 73+ onehanded swords for tyrannical etc..
##
##       Work on Optimising output, collapse multiblock into single with many basetypes.
##
## Item check order: Unique\RareRegal+Toptier\RareChaos+toptier\toptier\RareRegal6socketorchromatic\RareChaos6socketorchromatic
##                      \RareRegal\RareChaos\Chromatic\sixsocket\Flasks\Chisel(whiteonly)\Quality(whiteonly)\Tierbased sorting

class Item(object):
    """
    Base object contains collections of items and the relevant properties.
    Sets default values for use throughout the script.
    """
    backgroundcolor = "12 12 13 225"
    bordercolor = "0 0 0 0"
    defaultfontsize = 34
    mediumfontsize = 30
    smallfontsize = 19
    textcolor = "YouDidntSetATextColor"
    
    # Defaults to be used for all items depending on rarity.
    Rarity = {
        #Rarity: (background, border, fontsize, textcolor)
        'Unique': ("12 12 13 225", "175 96 37 225", 37, "175 96 37"),
        'Rare':   ("12 12 13 225", "255 255 119 50", 35, "255 255 119 225"),
        'Magic':  ("12 12 13 225", "136 136 255 50", 32, "136 136 255 225"),
        'Normal': ("12 12 13 225", "200 200 200 0", 27, "180 180 180 190")
              }
    
    # Values used to highlight certain items dependent on rarity.     
    Highlights = {
        #Rarity: (background, border, fontsize, textcolor)
        'Unique': ("12 12 13 225", "175 96 37 225", 37, "175 96 37"),
        'Rare':   ("12 12 13 225", "255 255 119 225", 35, "255 255 119 245"),
        'Magic':  ("12 12 13 225", "186 186 255 225", 35, "150 150 255 255"),
        'Normal': ("12 12 13 225", "200 200 200 225", 35, "225 225 225 245")
              }
    
    # Values used to lowlight certain items dependent on rarity.
    Lowlights = {
        #Rarity: (background, border, fontsize, textcolor)
        'Unique': ("12 12 13 225", "175 96 37 225", 37, "175 96 37"),
        'Rare':   ("12 12 13 225 150", "255 255 119 0", 34, "255 255 119 205"),
        'Magic':  ("12 12 13 225 120", "136 136 255 0", 30, "96 96 195 205"),
        'Normal': ("12 12 13 225 100", "200 200 200 0", 22, "160 160 160 150")
              }
    
    # Values used to denote certain conditions are met.
    Colors = {
        #Situation: (background, border, fontsize, textcolor, AlertSound)
        'Regal': (backgroundcolor, "150 0 255 255", defaultfontsize, textcolor),
        'Chaos': (backgroundcolor, "208 32 144 225", defaultfontsize, textcolor),
        'SixLink': ("230 107 26", "0 0 255", 45, textcolor, "1 300"),
        'FiveLink': ("230 107 26 200", "0 0 255", 40, textcolor),
        'TopTier': ("12 12 50 210", "10 150 30 100", defaultfontsize, textcolor),
        'Crafting': ("110 85 60 210", "110 85 60 210", defaultfontsize, textcolor),
        'Flasks': (backgroundcolor, "27 162 155", defaultfontsize, textcolor),
        'CurrentTier': ("12 40 13 225", "10 150 30 100", defaultfontsize, textcolor),
        'SecondTier': ("45 45 13 180", "150 150 20 0", defaultfontsize, textcolor),
        'ObsoleteTier': ("50 12 13 150", "100 19 19 0", defaultfontsize, textcolor),
        'HiddenTier': ("12 12 13 100", "12 12 13 0", smallfontsize, textcolor),
        }
    
    # List of top tier weapon types
    TopTierWeapons = [
        '"Gemini Claw"',
        '"Terror Claw"',
        '"Imperial Claw"',
        'Sai',
        '"Demon Dagger"',
        '"Imperial Skean"',
        '"Platinum Kris"',
        '"Profane Wand"',
        '"Prophecy Wand"',
        '"Tiger Hook"',
        '"Midnight Blade"',
        '"Eternal Sword"',
        '"Dragoon Sword"',
        '"Harpy Rapier"',
        '"Jewelled Foil"',
        '"Runic Hatchet"',
        '"Infernal Axe"',
        '"Behemoth Mace"',
        '"Nightmare Mace"',
        '"Maraketh Bow"',
        '"Harbinger Bow"',
        '"Imperial Bow"',
        '"Spine Bow"',
        '"Eclipse Staff"',
        '"Judgement Staff"',
        '"Exquisite Blade"',
        '"Infernal Sword"',
        '"Lion Sword"',
        'Fleshripper',
        '"Void Axe"',
        '"Coronal Maul"',
        '"Terror Maul"',
        '"Sambar Sceptre"',
        '"Void Sceptre"'
        ]
    
    # List of top tier armour types   
    TopTierArmour = [
        '"Titan Greaves"',
        '"Slink Boots"',
        '"Sorcerer Boots"',
        '"Dragonscale Boots"',
        '"Crusader Boots"',
        '"Murder Boots"',
        '"Titan Gauntlets"',
        '"Slink Gloves"',
        '"Sorcerer Gloves"',
        '"Dragonscale Gauntlets"',
        '"Crusader Gloves"',
        '"Murder Mitts"',
        '"Glorious Plate"',
        '"Assassin\'s Garb"',
        '"Vaal Regalia"',
        '"Triumphant Lamellar"',
        '"Saintly Chainmail"',
        '"Carnal Armour"',
        '"Eternal Burgonet"',
        '"Lion Pelt"',
        '"Hubris Circlet"',
        '"Nightmare Bascinet"',
        '"Praetor Crown"',
        '"Deicide Mask"',
        '"Pinnacle Tower Shield"',
        '"Imperial Buckler"',
        '"Titanium Spirit Shield"',
        '"Elegant Round Shield"',
        '"Archon Kite Shield"',
        '"Supreme Spiked Shield"',
        ]
    
    # List of top tier health and mana flasks
    TopTierFlasks = [
        '"Divine Life Flask"',
        '"Eternal Life Flask"',
        '"Eternal Mana Flask"',
        '"Divine Mana Flask"',
        '"Hallowed Hybrid Flask"'
        ]
        
    Claws = {
    # BaseType: (droplevel, next tier droplevel, obsolete level, good chromatic base 1 for yes 0 for no)
        '"Nailed Fist"': (3, 7, 12, 1),
        '"Sharktooth Claw"': (7, 12, 17, 1),
        'Awl': (12, 17, 22, 1),
        '"Cat\'s Paw"': (17, 22, 26, 1),
        'Blinder': (22, 26, 30, 1),
        '"Timeworn Claw"': (26, 30, 34, 1),
        '"Sparkling Claw"': (30, 34, 36, 1),
        '"Fright Claw"': (34, 36, 37, 1),
        '"Double Claw"': (36, 37, 40, 1),
        '"Thresher Claw"': (37, 40, 43, 1),
        'Gouger': (40, 43, 46, 1),
        '"Tiger\'s Paw"': (43, 46, 49, 1),
        '"Gut Ripper"': (46, 49, 52, 1),
        '"Prehistoric Claw"': (49, 52, 55, 1),
        '"Noble Claw"': (52, 55, 57, 1),
        '"Eagle Claw"': (55, 57, 58, 1),
        '"Twin Claw"': (57, 58, 60, 1),
        '"Great White Claw"': (58, 60, 62, 1),
        '"Throat Stabber"': (60, 62, 64, 1),
        '"Hellion\'s Paw"': (62, 64, 66, 1),
        '"Eye Gouger"': (64, 66, 68, 1),
        '"Vaal Claw"': (66, 68, 70, 1),
        '"Imperial Claw"': (68, 70, 72, 1),
        '"Terror Claw"': (70, 72, 100, 1),
        '"Gemini Claw"': (72, 100, 100, 1)
        }
        
    Wands = {
    # BaseType: (droplevel, next tier droplevel, obsolete level, good chromatic base 1 for yes 0 for no)
        '"Driftwood Wand"': (1, 6, 12, 1),
        '"Goat\'s Horn"': (6, 12, 18, 1),
        '"Carved Wand"': (12, 18, 24, 1),
        '"Quartz Wand"': (18, 24, 30, 1),
        '"Spiraled Wand"': (24, 30, 34, 1),
        '"Sage Wand"': (30, 34, 35, 1),
        '"Pagan Wand"': (34, 35, 40, 1),
        '"Faun\'s Horn"': (35, 40, 45, 1),
        '"Engraved Wand"': (40, 45, 49, 1),
        '"Crystal Wand"': (45, 49, 53, 1),
        '"Serpent Wand"': (49, 53, 55, 1),
        '"Omen Wand"': (53, 55, 56, 1),
        '"Heathen Wand"': (55, 56, 59, 1),
        '"Demon\'s Horn"': (56, 59, 62, 1),
        '"Imbued Wand"': (59, 62, 65, 1),
        '"Opal Wand"': (62, 65, 68, 1),
        '"Tornado Wand"': (65, 68, 70, 1),
        '"Prophecy Wand"': (68, 70, 100, 1),
        '"Profane Wand"': (70, 100, 100, 1)
        }
        
    Daggers = {
    # BaseType: (droplevel, next tier droplevel, obsolete level, good chromatic base 1 for yes 0 for no)
        '"Glass Shank"': (1, 5, 10, 1),
        '"Skinning Knife"': (5, 10, 15, 1),
        '"Carving Knife"': (10, 15, 20, 1),
        'Stiletto': (15, 20, 24, 1),
        '"Boot Knife"': (20, 24, 28, 1),
        '"Copper Kris"': (24, 28, 32, 1),
        'Skean': (28, 32, 36, 1),
        '"Imp Dagger"': (32, 36, 38, 1),
        '"Prong Dagger"': (36, 38, 41, 1),
        '"Flaying Knife"': (35, 38, 41, 1),
        '"Butcher Knife"': (38, 41, 44, 1),
        '"Poignard"': (41, 44, 47, 1),
        '"Boot Blade"': (44, 47, 50, 1),
        '"Golden Kris"': (47, 50, 53, 1),
        '"Royal Skean"': (50, 53, 55, 1),
        '"Fiend Dagger"': (53, 55, 56, 1),
        'Trisula': (55, 56, 58, 1),
        '"Gutting Knife"': (56, 58, 60, 1),
        '"Slaughter Knife"': (58, 60, 62, 1),
        'Ambusher': (60, 62, 64, 1),
        '"Ezomyte Dagger"': (62, 64, 66, 1),
        '"Platinum Kris"': (64, 66, 68, 1),
        '"Imperial Skean"': (66, 68, 70, 1),
        '"Demon Dagger"': (68, 70, 100, 1),
        'Sai': (70, 100, 100, 1)
        }
        
    OneHandSwords = {
    # BaseType: (droplevel, next tier droplevel, obsolete level, good chromatic base 1 for yes 0 for no)
        '"Rusted Sword"': (1, 5, 10, 1),
        '"Copper Sword"': (5, 10, 15, 1),
        'Sabre': (10, 15, 20, 1),
        '"Broad Sword"': (15, 20, 24, 0),
        '"War Sword"': (20, 24, 28, 0),
        '"Ancient Sword"': (24, 28, 32, 0),
        '"Elegant Sword"': (28, 32, 34, 0),
        '"Dusk Blade"': (32, 34, 35, 0),
        '"Hook Sword"': (34, 35, 38, 0),
        '"Variscite Blade"': (35, 38, 41, 1),
        'Cutlass': (38, 41, 44, 1),
        '"Baselard"': (41, 44, 47, 0),
        '"Battle Sword"': (44, 47, 50, 0),
        '"Elder Sword"': (47, 50, 53, 0),
        '"Graceful Sword"': (50, 53, 55, 0),
        '"Twilight Blade"': (53, 55, 56, 0),
        'Grappler': (55, 56, 58, 0),
        '"Gemstone Sword"': (56, 58, 60, 1),
        '"Corsair Sword"': (58, 60, 62, 1),
        'Gladius': (60, 62, 64, 0),
        '"Legion Sword"': (62, 64, 66, 0),
        '"Vaal Blade"': (64, 66, 68, 0),
        '"Eternal Sword"': (66, 68, 70, 0),
        '"Midnight Blade"': (68, 70, 100, 0),
        '"Tiger Hook"': (70, 100, 100, 0)
        }
    
    ThrustingOneHandSwords = {
    # BaseType: (droplevel, next tier droplevel, obsolete level, good chromatic base 1 for yes 0 for no)
        '"Rusted Spike"': (1, 7, 12, 1),
        '"Whalebone Rapier"': (7, 12, 17, 1),
        '"Battered Foil"': (12, 17, 22, 1),
        '"Basket Rapier"': (17, 22, 26, 1),
        '"Jagged Foil"': (22, 26, 30, 1),
        '"Antique Rapier"': (26, 30, 34, 1),
        '"Elegant Foil"': (30, 34, 36, 1),
        '"Thorn Rapier"': (34, 36, 37, 1),
        '"Smallsword"': (36, 37, 40, 1),
        '"Wyrmbone Rapier"': (37, 40, 43, 1),
        '"Burnished Foil"': (40, 43, 46, 1),
        'Estoc': (43, 46, 49, 1),
        '"Serrated Foil"': (46, 49, 52, 1),
        '"Primeval Rapier"': (49, 52, 55, 1),
        '"Fancy Foil"': (52, 55, 57, 1),
        '"Apex Rapier"': (55, 57, 58, 1),
        '"Courtesan Sword"': (57, 60, 62, 1),
        '"Dragonbone Rapier"': (58, 60, 62, 1),
        '"Tempered Foil"': (60, 62, 64, 1),
        'Pecoraro': (62, 64, 66, 1),
        '"Spiraled Foil"': (64, 66, 68, 1),
        '"Vaal Rapier"': (66, 68, 70, 1),
        '"Jewelled Foil"': (68, 70, 72, 1),
        '"Harpy Rapier"': (70, 72, 100, 1),
        '"Dragoon Sword"': (72, 100, 100, 1)
        }
    
    OneHandAxes = {
    # BaseType: (droplevel, next tier droplevel, obsolete level, good chromatic base 1 for yes 0 for no)
        '"Rusted Hatchet"': (1, 6, 11, 0),
        '"Jade Hatchet"': (6, 11, 16, 0),
        '"Boarding Axe"': (11, 16, 21, 0),
        'Cleaver': (16, 21, 25, 0),
        '"Broad Axe"': (21, 25, 29, 0),
        '"Arming Axe"': (25, 29, 33, 0),
        '"Decorative Axe"': (29, 33, 35, 0),
        '"Spectral Axe"': (33, 35, 36, 0),
        '"Etched Hatchet"': (35, 36, 39, 0),
        '"Jasper Axe"': (36, 39, 42, 0),
        'Tomahawk': (39, 42, 45, 0),
        '"Wrist Chopper"': (42, 45, 48, 0),
        '"War Axe"': (45, 48, 51, 0),
        '"Chest Splitter"': (48, 51, 54, 0),
        '"Ceremonial Axe"': (51, 54, 56, 0),
        '"Wraith Axe"': (54, 56, 57, 0),
        '"Engraved Hatchet"': (56, 57, 59, 0),
        '"Karui Axe"': (57, 59, 61, 0),
        '"Siege Axe"': (59, 61, 63, 0),
        '"Reaver Axe"': (61, 63, 65, 0),
        '"Butcher Axe"': (63, 65, 67, 0),
        '"Vaal Hatchet"': (65, 67, 69, 0),
        '"Royal Axe"': (67, 69, 71, 0),
        '"Infernal Axe"': (69, 71, 100, 0),
        '"Runic Hatchet"': (71, 100, 100, 0)
        }

    OneHandMaces = {
    # BaseType: (droplevel, next tier droplevel, obsolete level, good chromatic base 1 for yes 0 for no)
        '"Driftwood Club"': (1, 5, 10, 1),
        '"Tribal Club"': (5, 10, 15, 1),
        '"Spiked Club"': (10, 15, 20, 1),
        '"Stone Hammer"': (15, 20, 24, 0),
        '"War Hammer"': (20, 24, 28, 0),
        '"Bladed Mace"': (24, 28, 32, 0),
        '"Ceremonial Mace"': (28, 32, 34, 0),
        '"Dream Mace"': (32, 34, 35, 0),
        '"Wyrm Mace"': (34, 35, 38, 1),
        '"Petrified Club"': (35, 38, 41, 1),
        '"Barbed Club"': (38, 41, 44, 1),
        '"Rock Breaker"': (41, 44, 47, 0),
        '"Battle Hammer"': (44, 47, 50, 0),
        '"Flanged Mace"': (47, 50, 53, 0),
        '"Ornate Mace"': (50, 53, 55, 0),
        '"Phantom Mace"': (53, 55, 56, 0),
        '"Dragon Mace"': (55, 56, 58, 1),
        '"Ancestral Club"': (56, 58, 60, 1),
        'Tenderizer': (58, 60, 62, 1),
        'Gavel': (60, 62, 64, 0),
        '"Legion Hammer"': (62, 64, 66, 0),
        'Pernarch': (64, 66, 68, 0),
        '"Auric Mace"': (66, 68, 70, 0),
        '"Nightmare Mace"': (68, 70, 100, 0),
        '"Behemoth Mace"': (70, 100, 100, 0)
        }
    
    Bows = {
    # BaseType: (droplevel, next tier droplevel, obsolete level, good chromatic base 1 for yes 0 for no)
        '"Crude Bow"': (1, 5, 9, 0),
        '"Short Bow"': (5, 9, 14, 0),
        '"Long Bow"': (9, 14, 18, 0),
        '"Composite Bow"': (14, 18, 23, 0),
        '"Recurve Bow"': (18, 23, 28, 0),
        '"Bone Bow"': (23, 28, 32, 0),
        '"Royal Bow"': (28, 32, 35, 0),
        '"Death Bow"': (32, 35, 38, 0),
        '"Reflex Bow"': (36, 38, 41, 0),
        '"Grove Bow"': (35, 38, 41, 0),
        '"Decurve Bow"': (38, 41, 44, 0),
        '"Compound Bow"': (41, 44, 47, 0),
        '"Sniper Bow"': (44, 47, 50, 0),
        '"Ivory Bow"': (47, 50, 53, 0),
        '"Highborn Bow"': (50, 53, 56, 0),
        '"Decimation Bow"': (53, 56, 58, 0),
        '"Steelwood Bow"': (57, 58, 60, 0),
        '"Thicket Bow"': (56, 58, 60, 0),
        '"Citadel Bow"': (58, 60, 62, 0),
        '"Ranger Bow"': (60, 62, 64, 0),
        '"Assassin Bow"': (62, 64, 66, 0),
        '"Spine Bow"': (64, 66, 68, 0),
        '"Imperial Bow"': (66, 68, 71, 0),
        '"Harbinger Bow"': (68, 71, 100, 0),
        '"Maraketh Bow"': (71, 100, 100, 0)
        }
    
    Staves = {
    # BaseType: (droplevel, next tier droplevel, obsolete level, good chromatic base 1 for yes 0 for no)
        '"Gnarled Branch"': (1, 9, 13, 0),
        '"Primitive Staff"': (9, 13, 18, 0),
        '"Long Staff"': (13, 18, 23, 0),
        '"Iron Staff"': (18, 23, 28, 0),
        '"Coiled Staff"': (23, 28, 33, 0),
        '"Royal Staff"': (28, 33, 36, 0),
        '"Vile Staff"': (33, 36, 37, 0),
        '"Crescent Staff"': (36, 37, 41, 0),
        '"Woodful Staff"': (37, 41, 45, 0),
        'Quarterstaff': (41, 45, 49, 0),
        '"Military Staff"': (45, 49, 52, 0),
        '"Serpentine Staff"': (49, 52, 55, 0),
        '"Highborn Staff"': (52, 55, 57, 0),
        '"Foul Staff"': (55, 57, 58, 0),
        '"Moon Staff"': (57, 58, 60, 0),
        '"Primordial Staff"': (58, 60, 62, 0),
        '"Lathi"': (60, 62, 64, 0),
        '"Ezomyte Staff"': (62, 64, 66, 0),
        #'"Maelstrom Staff"': (64, 66, 68, 0), #Not Working need a workaround.
        '"Imperial Staff"': (66, 68, 70, 0),
        '"Judgement Staff"': (68, 70, 100, 0),
        '"Eclipse Staff"': (70, 100, 100, 0),
        }
    
    TwoHandSwords = {
    # BaseType: (droplevel, next tier droplevel, obsolete level, good chromatic base 1 for yes 0 for no)
        '"Corroded Blade"': (1, 8, 12, 0),
        'Longsword': (8, 12, 17, 0),
        '"Bastard Sword"': (12, 17, 22, 0),
        '"Two-Handed Sword"': (17, 22, 27, 0),
        '"Etched Greatsword"': (22, 27, 32, 0),
        '"Ornate Sword"': (27, 32, 35, 0),
        '"Spectral Sword"': (32, 35, 36, 0),
        '"Curved Blade"': (35, 36, 40, 0),
        '"Butcher Sword"': (36, 40, 44, 0),
        '"Footman Sword"': (40, 44, 48, 0),
        '"Highland Blade"': (44, 48, 51, 0),
        '"Engraved Greatsword"': (48, 51, 54, 0),
        '"Tiger Sword"': (51, 54, 56, 0),
        '"Wraith Sword"': (54, 56, 57, 0),
        '"Lithe Blade"': (56, 57, 59, 0),
        '"Headman\'s Sword"': (57, 59, 61, 0),
        '"Reaver Sword"': (59, 61, 63, 0),
        '"Ezomyte Blade"': (61, 63, 65, 0),
        '"Vaal Greatsword"': (63, 65, 67, 0),
        '"Lion Sword"': (65, 67, 70, 0),
        '"Infernal Sword"': (67, 70, 100, 0),
        '"Exquisite Blade"': (70, 100, 100, 0)
        }
    
    TwoHandAxes = {
    # BaseType: (droplevel, next tier droplevel, obsolete level, good chromatic base 1 for yes 0 for no)
        '"Stone Axe"': (1, 9, 13, 0),
        '"Jade Chopper"': (9, 13, 18, 0),
        'Woodsplitter': (13, 18, 23, 0),
        'Poleaxe': (18, 23, 28, 0),
        '"Double Axe"': (23, 28, 33, 0),
        '"Gilded Axe"': (28, 33, 37, 0),
        '"Shadow Axe"': (33, 37, 41, 0),
        '"Jasper Chopper"': (37, 41, 45, 0),
        '"Dagger Axe"': (36, 41, 45, 0),
        '"Timber Axe"': (41, 45, 49, 0),
        '"Headsman Axe"': (45, 49, 52, 0),
        'Labrys': (49, 52, 55, 0),
        '"Noble Axe"': (52, 55, 59, 0),
        '"Abyssal Axe"': (55, 59, 60, 0),
        '"Talon Axe"': (59, 60, 62, 0),
        '"Karui Chopper"': (58, 60, 62, 0),
        '"Sundering Axe"': (60, 62, 64, 0),
        '"Ezomyte Axe"': (62, 64, 66, 0),
        '"Vaal Axe"': (64, 66, 68, 0),
        '"Despot Axe"': (66, 68, 70, 0),
        '"Void Axe"': (68, 70, 100, 0),
        'Fleshripper': (70, 100, 100, 0)
        }
    
    TwoHandMaces = {
    # BaseType: (droplevel, next tier droplevel, obsolete level, good chromatic base 1 for yes 0 for no)
        '"Driftwood Maul"': (3, 8, 12, 0),
        '"Tribal Maul"': (8, 12, 17, 0),
        'Mallet': (12, 17, 22, 0),
        'Sledgehammer': (17, 22, 27, 0),
        '"Jagged Maul"': (22, 27, 32, 0),
        '"Brass Maul"': (27, 32, 34, 0),
        '"Fright Maul"': (32, 34, 36, 0),
        '"Morning Star"': (34, 36, 40, 0),
        '"Totemic Maul"': (36, 40, 44, 0),
        '"Great Mallet"': (40, 44, 48, 0),
        'Steelhead': (44, 48, 51, 0),
        '"Spiny Maul"': (48, 51, 54, 0),
        '"Plated Maul"': (51, 54, 56, 0),
        '"Dread Maul"': (54, 57, 59, 0),
        'Solar Maul': (56, 59, 61, 0),
        '"Karui Maul"': (57, 59, 61, 0),
        '"Colossus Mallet"': (59, 61, 63, 0),
        'Piledriver': (61, 63, 65, 0),
        'Meatgrinder': (63, 65, 67, 0),
        '"Imperial Maul"': (65, 67, 69, 0),
        '"Terror Maul"': (67, 69, 100, 0),
        '"Coronal Maul"': (69, 100, 100, 0)
        }
    
    Sceptres = {
    # BaseType: (droplevel, next tier droplevel, obsolete level, good chromatic base 1 for yes 0 for no)
        '"Driftwood Sceptre"': (1, 5, 10, 1),
        '"Darkwood Sceptre"': (5, 10, 15, 0),
        '"Bronze Sceptre"': (10, 15, 20, 0),
        '"Quartz Sceptre"': (15, 20, 24, 0),
        '"Iron Sceptre"': (20, 24, 28, 0),
        '"Ochre Sceptre"': (24, 28, 32, 0),
        '"Ritual Sceptre"': (28, 32, 36, 0),
        '"Shadow Sceptre"': (32, 36, 38, 0),
        '"Horned Sceptre"': (36, 38, 41, 0),
        '"Grinning Fetish"': (35, 38, 41, 0),
        'Sekhem': (38, 41, 44, 0),
        '"Crystal Sceptre"': (41, 44, 47, 0),
        '"Lead Sceptre"': (44, 47, 50, 0),
        '"Blood Sceptre"': (47, 50, 53, 0),
        '"Royal Sceptre"': (50, 53, 56, 0),
        '"Abyssal Sceptre"': (53, 56, 58, 0),
        '"Stag Sceptre"': (55, 58, 60, 0),
        '"Karui Sceptre"': (56, 58, 60, 0),
        '"Tyrant\'s Sekhem"': (58, 60, 62, 0),
        '"Opal Sceptre"': (60, 62, 64, 0),
        '"Platinum Sceptre"': (62, 64, 66, 0),
        '"Vaal Sceptre"': (64, 66, 68, 0),
        '"Carnal Sceptre"': (66, 68, 70, 0),
        '"Void Sceptre"': (68, 70, 100, 0),
        '"Sambar Sceptre"': (70, 100, 100, 0)
        }
    
    Gloves = {
    # BaseType: (droplevel, next tier droplevel, obsolete level, good chromatic base 1 for yes 0 for no)
        '"Iron Gauntlets"': (1, 11, 23, 1),
        '"Plated Gauntlets"': (11, 23, 35, 1),
        '"Bronze Gauntlets"': (23, 35, 39, 1),
        '"Steel Gauntlets"': (35, 39, 47, 1),
        '"Antique Gauntlets"': (39, 47, 53, 1),
        '"Ancient Gauntlets"': (47, 53, 63, 1),
        '"Goliath Gauntlets"': (53, 63, 69, 1),
        '"Vaal Gauntlets"': (63, 69, 100, 1),
        '"Titan Gauntlets"': (69, 100, 100, 1),
        '"Rawhide Gloves"': (1, 9, 21, 1),
        '"Goathide Gloves"': (9, 21, 33, 1),
        '"Deerskin Gloves"': (21, 33, 38, 1),
        '"Nubuck Gloves"': (33, 38, 45, 1),
        '"Eelskin Gloves"': (38, 45, 54, 1),
        '"Sharkskin Gloves"': (45, 54, 62, 1),
        '"Shagreen Gloves"': (54, 62, 70, 1),
        '"Stealth Gloves"': (62, 70, 100, 1),
        '"Slink Gloves"': (70, 100, 100, 1),
        '"Wool Gloves"': (1, 12, 25, 1),
        '"Velvet Gloves"': (12, 25, 36, 1),
        '"Silk Gloves"': (25, 36, 41, 1),
        '"Embroidered Gloves"': (36, 41, 47, 1),
        '"Satin Gloves"': (41, 47, 55, 1),
        '"Samite Gloves"': (47, 55, 60, 1),
        '"Conjurer Gloves"': (55, 60, 69, 1),
        '"Arcanist Gloves"': (60, 69, 100, 1),
        '"Sorcerer Gloves"': (69, 100, 100, 1),
        '"Fishscale Gauntlets"': (1, 15, 27, 1),
        '"Ironscale Gauntlets"': (15, 27, 36, 1),
        '"Bronzescale Gauntlets"': (27, 36, 43, 1),
        '"Steelscale Gauntlets"': (36, 43, 49, 1),
        '"Serpentscale Gauntlets"': (43, 49, 59, 1),
        '"Wyrmscale Gauntlets"': (49, 59, 67, 1),
        '"Hydrascale Gauntlets"': (59, 67, 100, 1),
        '"Dragonscale Gauntlets"': (67, 100, 100, 1),
        '"Chain Gloves"': (7, 19, 32, 1),
        '"Ringmail Gloves"': (19, 32, 37, 1),
        '"Mesh Gloves"': (32, 37, 43, 1),
        '"Riveted Gloves"': (37, 43, 51, 1),
        '"Zealot Gloves"': (43, 51, 57, 1),
        '"Soldier Gloves"': (51, 57, 66, 1),
        '"Legion Gloves"': (57, 66, 100, 1),
        '"Crusader Gloves"': (66, 100, 100, 1),
        '"Wrapped Mitts"': (5, 16, 31, 1),
        '"Strapped Mitts"': (16, 31, 36, 1),
        '"Clasped Mitts"': (31, 36, 45, 1),
        '"Trapper Mitts"': (36, 45, 50, 1),
        '"Ambush Mitts"': (45, 50, 58, 1),
        '"Carnal Mitts"': (50, 58, 67, 1),
        '"Assassin\'s Mitts"': (58, 67, 100, 1),
        '"Murder Mitts"': (67, 100, 100, 1)
        }
    
    Boots = {
    # BaseType: (droplevel, next tier droplevel, obsolete level, good chromatic base 1 for yes 0 for no)
        '"Iron Greaves"': (1, 9, 23, 1),
        '"Steel Greaves"': (9, 23, 33, 1),
        '"Plated Greaves"': (23, 33, 37, 1),
        '"Reinforced Greaves"': (33, 37, 46, 1),
        '"Antique Greaves"': (37, 46, 54, 1),
        '"Ancient Greaves"': (46, 54, 62, 1),
        '"Goliath Greaves"': (54, 62, 68, 1),
        '"Vaal Greaves"': (62, 68, 100, 1),
        '"Titan Greaves"': (68, 100, 100, 1),
        '"Rawhide Boots"': (1, 12, 22, 1),
        '"Goathide Boots"': (12, 22, 34, 1),
        '"Deerskin Boots"': (22, 34, 39, 1),
        '"Nubuck Boots"': (34, 39, 44, 1),
        '"Eelskin Boots"': (39, 44, 55, 1),
        '"Sharkskin Boots"': (44, 55, 62, 1),
        '"Shagreen Boots"': (55, 62, 69, 1),
        '"Stealth Boots"': (62, 69, 100, 1),
        '"Slink Boots"': (69, 100, 100, 1),
        '"Wool Shoes"': (1, 9, 22, 1),
        '"Velvet Slippers"': (9, 22, 32, 1),
        '"Silk Slippers"': (22, 32, 38, 1),
        '"Scholar Boots"': (32, 38, 44, 1),
        '"Satin Slippers"': (38, 44, 53, 1),
        '"Samite Slippers"': (44, 53, 61, 1),
        '"Conjurer Boots"': (53, 61, 67, 1),
        '"Arcanist Slippers"': (61, 67, 100, 1),
        '"Sorcerer Boots"': (67, 100, 100, 1),
        '"Leatherscale Boots"': (6, 18, 30, 1),
        '"Ironscale Boots"': (18, 30, 36, 1),
        '"Bronzescale Boots"': (30, 36, 42, 1),
        '"Steelscale Boots"': (36, 42, 51, 1),
        '"Serpentscale Boots"': (42, 51, 59, 1),
        '"Wyrmscale Boots"': (51, 59, 65, 1),
        '"Hydrascale Boots"': (59, 65, 100, 1),
        '"Dragonscale Boots"': (65, 100, 100, 1),
        '"Chain Boots"': (5, 13, 28, 1),
        '"Ringmail Boots"': (13, 28, 36, 1),
        '"Mesh Boots"': (28, 36, 40, 1),
        '"Riveted Boots"': (36, 40, 49, 1),
        '"Zealot Boots"': (40, 49, 58, 1),
        '"Soldier Boots"': (49, 58, 64, 1),
        '"Legion Boots"': (58, 64, 100, 1),
        '"Crusader Boots"': (64, 100, 100, 1),
        '"Wrapped Boots"': (6, 16, 27, 1),
        '"Strapped Boots"': (16, 27, 34, 1),
        '"Clasped Boots"': (27, 34, 41, 1),
        '"Shackled Boots"': (34, 41, 47, 1),
        '"Trapper Boots"': (41, 47, 55, 1),
        '"Ambush Boots"': (47, 55, 63, 1),
        '"Carnal Boots"': (55, 63, 69, 1),
        '"Assassin\'s Boots"': (63, 69, 100, 1),
        '"Murder Boots"': (69, 100, 100, 1)
        }
    
    BodyArmour = {
    # BaseType: (droplevel, next tier droplevel, obsolete level, good chromatic base 1 for yes 0 for no)
        '"Plate Vest"': (1, 6, 17, 0),
        'Chestplate': (6, 17, 21, 0),
        '"Copper Plate"': (17, 21, 28, 0),
        '"War Plate"': (21, 28, 32, 0),
        '"Full Plate"': (28, 32, 35, 0),
        '"Arena Plate"': (32, 35, 37, 0),
        '"Lordly Plate"': (35, 37, 41, 0),
        '"Bronze Plate"': (37, 41, 45, 0),
        '"Battle Plate"': (41, 45, 49, 0),
        '"Sun Plate"': (45, 49, 53, 0),
        '"Colosseum Plate"': (49, 53, 56, 0),
        '"Majestic Plate"': (53, 56, 59, 0),
        '"Golden Plate"': (56, 59, 62, 0),
        '"Crusader Plate"': (59, 62, 65, 0),
        '"Astral Plate"': (62, 65, 68, 0),
        '"Gladiator Plate"': (65, 68, 100, 0),
        '"Glorious Plate"': (68, 100, 100, 0),
        '"Kaom\'s Plate"': (1, 100, 100, 0),
        '"Shabby Jerkin"': (2, 9, 17, 0),
        '"Strapped Leather"': (9, 17, 25, 0),
        '"Buckskin Tunic"': (17, 25, 28, 0),
        '"Wild Leather"': (25, 28, 32, 0),
        '"Full Leather"': (28, 32, 35, 0),
        '"Sun Leather"': (32, 35, 37, 0),
        '"Thief\'s Garb"': (35, 37, 41, 0),
        '"Eelskin Tunic"': (37, 41, 45, 0),
        '"Frontier Leather"': (41, 45, 49, 0),
        '"Glorious Leather"': (45, 49, 53, 0),
        '"Coronal Leather"': (49, 53, 56, 0),
        '"Cutthroat\'s Garb"': (53, 56, 59, 0),
        '"Sharkskin Tunic"': (56, 59, 62, 0),
        '"Destiny Leather"': (59, 62, 65, 0),
        '"Exquisite Leather"': (62, 65, 68, 0),
        '"Zodiac Leather"': (65, 68, 100, 0),
        '"Assassin\'s Garb"': (68, 100, 100, 0),
        '"Simple Robe"': (3, 11, 18, 0),
        '"Silken Vest"': (11, 18, 25, 0),
        '"Scholar\'s Robe"': (18, 25, 28, 0),
        '"Silken Garb"': (25, 28, 32, 0),
        '"Mage\'s Vestment"': (28, 32, 25, 0),
        '"Silk Robe"': (32, 35, 37, 0),
        '"Cabalist Regalia"': (35, 37, 41, 0),
        '"Sage\'s Robe"': (37, 41, 45, 0),
        '"Silken Wrap"': (41, 45, 49, 0),
        '"Conjurer\'s Vestment"': (45, 49, 53, 0),
        '"Spidersilk Robe"': (49, 53, 56, 0),
        '"Destroyer Regalia"': (53, 56, 59, 0),
        '"Savant\'s Robe"': (56, 59, 62, 0),
        '"Necromancer Silks"': (59, 62, 65, 0),
        '"Occultist\'s Vestment"': (62, 65, 68, 0),
        '"Widowsilk Robe"': (65, 68, 100, 0),
        '"Vaal Regalia"': (68, 100, 100, 0),
        '"Scale Vest"': (4, 8, 17, 0),
        '"Light Brigandine"': (8, 17, 21, 0),
        '"Scale Doublet"': (17, 21, 28, 0),
        '"Infantry Brigandine"': (21, 28, 32, 0),
        '"Full Scale Armour"': (28, 32, 35, 0),
        '"Soldier\'s Brigandine"': (32, 35, 38, 0),
        '"Field Lamellar"': (35, 38, 42, 0),
        '"Wyrmscale Doublet"': (38, 42, 46, 0),
        '"Hussar Brigandine"': (42, 46, 50, 0),
        '"Full Wyrmscale"': (46, 50, 54, 0),
        '"Commander\'s Brigandine"': (50, 54, 57, 0),
        '"Battle Lamellar"': (54, 57, 60, 0),
        '"Dragonscale Doublet"': (57, 60, 63, 0),
        '"Desert Brigandine"': (60, 63, 66, 0),
        '"Full Dragonscale"': (63, 66, 69, 0),
        '"General\'s Brigandine"': (66, 69, 100, 0),
        '"Triumphant Lamellar"': (69, 100, 100, 0),
        '"Chainmail Vest"': (4, 8, 17, 0),
        '"Chainmail Tunic"': (8, 17, 21, 0),
        '"Ringmail Coat"': (17, 21, 28, 0),
        '"Chainmail Doublet"': (21, 28, 32, 0),
        '"Full Ringmail"': (28, 32, 35, 0),
        '"Full Chainmail"': (32, 35, 39, 0),
        '"Holy Chainmail"': (35, 39, 43, 0),
        '"Latticed Ringmail"': (39, 43, 47, 0),
        '"Crusader Chainmail"': (43, 47, 51, 0),
        '"Ornate Ringmail"': (47, 51, 55, 0),
        '"Chain Hauberk"': (51, 55, 58, 0),
        '"Devout Chainmail"': (55, 58, 61, 0),
        '"Loricated Ringmail"': (58, 61, 64, 0),
        '"Conquest Chainmail"': (61, 64, 67, 0),
        '"Elegant Ringmail"': (64, 67, 70, 0),
        '"Saint\'s Hauberk"': (67, 70, 100, 0),
        '"Saintly Chainmail"': (70, 100, 100, 0),
        '"Padded Vest"': (4, 9, 18, 0),
        '"Oiled Vest"': (9, 18, 22, 0),
        '"Padded Jacket"': (18, 22, 28, 0),
        '"Oiled Coat"': (22, 28, 32, 0),
        '"Scarlet Raiment"': (28, 32, 35, 0),
        '"Waxed Garb"': (32, 35, 40, 0),
        '"Bone Armour"': (35, 40, 44, 0),
        '"Quilted Jacket"': (40, 44, 48, 0),
        '"Sleek Coat"': (44, 48, 52, 0),
        '"Crimson Raiment"': (48, 52, 56, 0),
        '"Lacquered Garb"': (52, 56, 59, 0),
        '"Crypt Armour"': (56, 59, 62, 0),
        '"Sentinel Jacket"': (59, 62, 65, 0),
        '"Varnished Coat"': (62, 65, 68, 0),
        '"Blood Raiment"': (65, 68, 71, 0),
        '"Sadist Garb"': (68, 71, 100, 0),
        '"Carnal Armour"': (71, 100, 100, 0)
        }
    
    Helmets = {
    # BaseType: (droplevel, next tier droplevel, obsolete level, good chromatic base 1 for yes 0 for no)
        '"Iron Hat"': (1, 7, 18, 1),
        '"Cone Helmet"': (7, 18, 26, 1),
        '"Barbute Helmet"': (18, 26, 35, 1),
        '"Close Helmet"': (26, 35, 40, 1),
        '"Gladiator Helmet"': (35, 40, 48, 1),
        '"Reaver Helmet"': (40, 48, 55, 1),
        '"Siege Helmet"': (48, 55, 60, 1),
        '"Samite Helmet"': (55, 60, 65, 1),
        '"Ezomyte Burgonet"': (60, 65, 69, 1),
        '"Royal Burgonet"': (65, 69, 100, 1),
        '"Eternal Burgonet"': (69, 100, 100, 1),
        '"Leather Cap"': (3, 10, 20, 1),
        '"Tricorne"': (10, 20, 30, 1),
        '"Leather Hood"': (20, 30, 41, 1),
        '"Wolf Pelt"': (30, 41, 47, 1),
        '"Hunter Hood"': (41, 47, 55, 1),
        '"Noble Tricorne"': (47, 55, 60, 1),
        '"Ursine Pelt"': (55, 60, 64, 1),
        '"Silken Hood"': (60, 64, 70, 1),
        '"Sinner Tricorne"': (64, 70, 100, 1),
        '"Lion Pelt"': (70, 100, 100, 1),
        '"Vine Circlet"': (3, 8, 17, 1),
        '"Iron Circlet"': (8, 17, 26, 1),
        '"Torture Cage"': (17, 26, 34, 1),
        '"Tribal Circlet"': (26, 34, 39, 1),
        '"Bone Circlet"': (34, 39, 48, 1),
        '"Lunaris Circlet"': (39, 48, 54, 1),
        '"Steel Circlet"': (48, 54, 59, 1),
        '"Necromancer Circlet"': (54, 59, 65, 1),
        '"Solaris Circlet"': (59, 65, 69, 1),
        '"Mind Cage"': (65, 69, 100, 1),
        '"Hubris Circlet"': (69, 100, 100, 1),
        '"Battered Helm"': (4, 13, 23, 1),
        'Sallet': (13, 23, 33, 1),
        '"Visored Sallet"': (23, 33, 36, 1),
        '"Gilded Sallet"': (33, 36, 43, 1),
        '"Secutor Helm"': (36, 43, 51, 1),
        '"Fencer Helm"': (43, 51, 58, 1),
        '"Lacquered Helmet"': (51, 58, 63, 1),
        '"Fluted Bascinet"': (58, 63, 67, 1),
        '"Pig-Faced Bascinet"': (63, 67, 100, 1),
        '"Nightmare Bascinet"': (67, 100, 100, 1),
        '"Rusted Coif"': (5, 12, 22, 1),
        '"Soldier Helmet"' : (12, 22, 31, 1),
        '"Great Helmet"': (22, 31, 37, 1),
        '"Crusader Helmet"': (31, 37, 44, 1),
        '"Aventail Helmet"': (37, 44, 53, 1),
        '"Zealot Helmet"': (44, 53, 58, 1),
        '"Great Crown"': (53, 58, 63, 1),
        '"Magistrate Crown"': (58, 63, 68, 1),
        '"Prophet Crown"': (63, 68, 100, 1),
        '"Praetor Crown"': (68, 100, 100, 1),
        '"Scare Mask"': (4, 10, 17, 1),
        '"Plague Mask"': (10, 17, 28, 1),
        '"Iron Mask"': (17, 28, 35, 1),
        '"Festival Mask"': (28, 35, 38, 1),
        '"Golden Mask"': (35, 38, 45, 1),
        '"Raven Mask"': (38, 45, 52, 1),
        '"Callous Mask"': (45, 52, 57, 1),
        '"Regicide Mask"': (52, 57, 62, 1),
        '"Harlequin Mask"': (57, 62, 67, 1),
        '"Vaal Mask"': (62, 67, 100, 1),
        '"Deicide Mask"': (67, 100, 100, 1)
        }
    
    Shields = {
    # BaseType: (droplevel, next tier droplevel, obsolete level, good chromatic base 1 for yes 0 for no)
        '"Splintered Tower Shield"': (1, 5, 11, 0),
        '"Corroded Tower Shield"': (5, 11, 17, 0),
        '"Rawhide Tower Shield"': (11, 17, 24, 0),
        '"Cedar Tower Shield"': (17, 24, 30, 0),
        '"Copper Tower Shield"': (24, 30, 35, 0),
        '"Reinforced Tower Shield"': (30, 35, 39, 0),
        '"Painted Tower Shield"': (35, 39, 43, 0),
        '"Buckskin Tower Shield"': (39, 43, 47, 0),
        '"Mahogany Tower Shield"': (43, 47, 51, 0),
        '"Bronze Tower Shield"': (47, 51, 55, 0),
        '"Girded Tower Shield"': (51, 55, 58, 0),
        '"Crested Tower Shield"': (55, 58, 61, 0),
        '"Shagreen Tower Shield"': (58, 61, 64, 0),
        '"Ebony Tower Shield"': (61, 64, 67, 0),
        '"Ezomyte Tower Shield"': (64, 67, 70, 0),
        '"Colossal Tower Shield"': (67, 70, 100, 0),
        '"Pinnacle Tower Shield"': (70, 100, 100, 0),
        '"Goathide Buckler"': (1, 8, 16, 1),
        '"Pine Buckler"': (8, 16, 23, 1),
        '"Painted Buckler"': (16, 23, 29, 1),
        '"Hammered Buckler"': (23, 29, 34, 1),
        '"War Buckler"': (29, 34, 38, 1),
        '"Gilded Buckler"': (34, 38, 42, 1),
        '"Oak Buckler"': (38, 42, 46, 1),
        '"Enameled Buckler"': (42, 46, 50, 1),
        '"Corrugated Buckler"': (46, 50, 54, 1),
        '"Battle Buckler"': (50, 54, 57, 1),
        '"Golden Buckler"': (54, 57, 60, 1),
        '"Ironwood Buckler"': (57, 60, 63, 1),
        '"Lacquered Buckler"': (60, 63, 66, 1),
        '"Vaal Buckler"': (63, 66, 69, 1),
        '"Crusader Buckler"': (66, 69, 100, 1),
        '"Imperial Buckler"': (69, 100, 100, 1),
        '"Twig Spirit Shield"': (1, 9, 15, 1),
        '"Yew Spirit Shield"': (9, 15, 23, 1),
        '"Bone Spirit Shield"': (15, 23, 28, 1),
        '"Tarnished Spirit Shield"': (23, 28, 33, 1),
        '"Jingling Spirit Shield"': (28, 33, 37, 1),
        '"Brass Spirit Shield"': (33, 37, 41, 1),
        '"Walnut Spirit Shield"': (37, 41, 45, 1),
        '"Ivory Spirit Shield"': (41, 45, 49, 1),
        '"Ancient Spirit Shield"': (45, 49, 53, 1),
        '"Chiming Spirit Shield"': (49, 53, 56, 1),
        '"Thorium Spirit Shield"': (53, 56, 59, 1),
        '"Lacewood Spirit Shield"': (56, 59, 62, 1),
        '"Fossilised Spirit Shield"': (59, 62, 65, 1),
        '"Vaal Spirit Shield"': (62, 65, 68, 1),
        '"Harmonic Spirit Shield"': (65, 68, 100, 1),
        '"Titanium Spirit Shield"': (68, 100, 100, 1),
        '"Rotted Round Shield"': (5, 12, 20, 0),
        '"Fir Round Shield"': (12, 20, 27, 0),
        '"Studded Round Shield"': (20, 27, 33, 0),
        '"Scarlet Round Shield"': (27, 33, 39, 0),
        '"Splendid Round Shield"': (33, 39, 45, 0),
        '"Maple Round Shield"': (39, 45, 49, 0),
        '"Spiked Round Shield"': (45, 49, 54, 0),
        '"Crimson Round Shield"': (49, 54, 58, 0),
        '"Baroque Round Shield"': (54, 58, 62, 0),
        '"Teak Round Shield"': (58, 62, 66, 0),
        '"Spiny Round Shield"': (62, 66, 70, 0),
        '"Cardinal Round Shield"': (66, 70, 100, 0),
        '"Elegant Round Shield"': (70, 100, 100, 0),
        '"Plank Kite Shield"': (7, 13, 20, 0),
        '"Linden Kite Shield"': (13, 20, 27, 0),
        '"Reinforced Kite Shield"': (20, 27, 34, 0),
        '"Layered Kite Shield"': (27, 34, 40, 0),
        '"Ceremonial Kite Shield"': (34, 40, 46, 0),
        '"Etched Kite Shield"': (40, 46, 50, 0),
        '"Steel Kite Shield"': (46, 50, 55, 0),
        '"Laminated Kite Shield"': (50, 55, 59, 0),
        '"Angelic Kite Shield"': (55, 59, 62, 0),
        '"Branded Kite Shield"': (59, 62, 65, 0),
        '"Champion Kite Shield"': (62, 65, 68, 0),
        '"Mosaic Kite Shield"': (65, 68, 100, 0),
        '"Archon Kite Shield"': (68, 100, 100, 0),
        '"Spiked Bundle"': (5, 12, 20, 1),
        '"Driftwood Spiked Shield"': (12, 20, 27, 1),
        '"Alloyed Spiked Shield"': (20, 27, 33, 1),
        '"Burnished Spiked Shield"': (27, 33, 39, 1),
        '"Ornate Spiked Shield"': (33, 39, 45, 1),
        '"Redwood Spiked Shield"': (39, 45, 49, 1),
        '"Compound Spiked Shield"': (45, 49, 54, 1),
        '"Polished Spiked Shield"': (49, 54, 58, 1),
        '"Sovereign Spiked Shield"': (54, 58, 62, 1),
        '"Alder Spiked Shield"': (58, 62, 66, 1),
        '"Ezomyte Spiked Shield"': (62, 66, 70, 1),
        '"Mirrored Spiked Shield"': (66, 70, 100, 1),
        '"Supreme Spiked Shield"': (70, 100, 100, 1)        
        }
        
    Flasks = {
    # BaseType: (droplevel, next tier droplevel, obsolete level)
        '"Small Life Flask"': (0, 3, 6),
        '"Small Mana Flask"': (0, 3, 6),
        '"Small Hybrid Flask"': (10, 20, 30),
        '"Medium Life Flask"': (3, 6, 12),
        '"Medium Mana Flask"': (3, 6, 12),
        '"Medium Hybrid Flask"': (20, 30, 40),
        '"Large Life Flask"': (6, 12, 18),
        '"Large Mana Flask"': (6, 12, 18),
        '"Large Hybrid Flask"': (30, 40, 50),
        '"Greater Life Flask"': (12, 18, 24),
        '"Greater Mana Flask"': (12, 18, 24),
        '"Grand Life Flask"': (18, 24, 30),
        '"Grand Mana Flask"': (18, 24, 30),
        '"Giant Life Flask"': (24, 30, 36),
        '"Giant Mana Flask"': (24, 30, 36),
        '"Colossal Life Flask"': (30, 36, 42),
        '"Colossal Mana Flask"': (30, 36, 42),
        '"Colossal Hybrid Flask"': (40, 50, 60),
        '"Sacred Life Flask"': (36, 42, 50),
        '"Sacred Mana Flask"': (36, 42, 50),
        '"Sacred Hybrid Flask"': (50, 60, 100),
        '"Hallowed Life Flask"': (42, 50, 100),
        '"Hallowed Mana Flask"': (42, 50, 100),
        '"Hallowed Hybrid Flask"': (60, 100, 100),
        '"Sanctified Life Flask"': (50, 65, 100),
        '"Sanctified Mana Flask"': (50, 65, 100),
        '"Divine Life Flask"': (60, 100, 100),
        '"Divine Mana Flask"': (60, 100, 100),
        '"Eternal Life Flask"': (65, 100, 100),
        '"Eternal Mana Flask"': (65, 100, 100)
        }

    UtilityFlasks = {
    # BaseType: tier
        '"Diamond Flask"': 1,
        '"Ruby Flask"': 0,
        '"Sapphire Flask"': 0,
        '"Topaz Flask"': 0,
        '"Granite Flask"': 1,
        '"Quicksilver Flask"': 0,
        '"Amethyst Flask"': 0,
        '"Quartz Flask"': 0,
        '"Jade Flask"': 1,
        '"Basalt Flask"': 0,
        '"Aquamarine Flask"': 0,
        '"Stibnite Flask"': 0,
        '"Sulphur Flask"': 0,
        '"Silver Flask"': 0,
        '"Bismuth Flask"': 0,        
        }
        
    Amulets = [
        '"Paua Amulet"',
        '"Coral Amulet"',
        '"Amber Amulet"',
        '"Jade Amulet"',
        '"Lapis Amulet"',
        '"Gold Amulet"',
        '"Onyx Amulet"',
        '"Turquoise Amulet"',
        '"Agate Amulet"',
        '"Citrine Amulet"',
        '"Jet Amulet"',
        'Talisman',
        ]
    
    Rings = [
        '"Iron Ring"',
        '"Coral Ring"',
        '"Paua Ring"',
        '"Gold Ring"',
        '"Topaz Ring"',
        '"Sapphire Ring"',
        '"Ruby Ring"',
        '"Prismatic Ring"',
        '"Moonstone Ring"',
        '"Amethyst Ring"',
        '"Diamond Ring"',
        '"Two-Stone Ring"',
        '"Unset Ring"'
        ]
    
    Belts = [
        '"Rustic Sash"',
        '"Chain Belt"',
        '"Leather Belt"',
        '"Heavy Belt"',
        '"Cloth Belt"',
        '"Studded Belt"'
        ]
        
    Quivers = [
        '"Cured Quiver"',
        '"Rugged Quiver"',
        '"Conductive Quiver"',
        '"Heavy Quiver"',
        '"Light Quiver"',
        '"Serrated Arrow Quiver"',
        '"Two-Point Arrow Quiver"',
        '"Sharktooth Arrow Quiver"',
        '"Blunt Arrow Quiver"',
        '"Fire Arrow Quiver"',
        '"Broadhead Arrow Quiver"',
        '"Penetrating Arrow Quiver"',
        '"Spike-Point Arrow Quiver"'
        ]
    
    ItemClasses = [
        Wands,
        Sceptres,
        Claws,
        Daggers,
        OneHandSwords,
        ThrustingOneHandSwords,
        OneHandAxes,
        OneHandMaces,
        Bows,
        Staves,
        TwoHandSwords,
        TwoHandAxes,
        TwoHandMaces,
        Gloves,
        Boots,
        BodyArmour,
        Helmets,
        Shields
        ]

    NoDropLevelItemClasses = [
        #Wands,
        #Sceptres
        ]
        
    JewelleryClasses = [
        Amulets,
        Rings,
        Quivers,
        Belts
        ]
        
    ValuableJewellery = [
        '"Paua Amulet"',
        '"Amber Amulet"',
        '"Jade Amulet"',
        '"Lapis Amulet"',
        '"Gold Amulet"',
        '"Onyx Amulet"',
        '"Turquoise Amulet"',
        '"Agate Amulet"',
        '"Citrine Amulet"',
        '"Jet Amulet"',
        'Talisman',
        '"Iron Ring"',
        '"Coral Ring"',
        '"Gold Ring"',
        '"Topaz Ring"',
        '"Sapphire Ring"',
        '"Ruby Ring"',
        '"Prismatic Ring"',
        '"Moonstone Ring"',
        '"Amethyst Ring"',
        '"Diamond Ring"',
        '"Two-Stone Ring"',
        '"Unset Ring"',
        '"Rustic Sash"',
        '"Chain Belt"',
        '"Leather Belt"',
        '"Heavy Belt"',
        '"Cured Quiver"',
        '"Rugged Quiver"',
        '"Conductive Quiver"',
        '"Heavy Quiver"',
        '"Light Quiver"',
        '"Serrated Arrow Quiver"',
        '"Two-Point Arrow Quiver"',
        '"Sharktooth Arrow Quiver"',
        '"Blunt Arrow Quiver"',
        '"Fire Arrow Quiver"',
        '"Broadhead Arrow Quiver"',
        '"Penetrating Arrow Quiver"',
        '"Spike-Point Arrow Quiver"'
        ]
    

##############################################################################
        
class Currency(Item):
        
    backgroundcolor = Item.backgroundcolor
    bordercolor = Item.bordercolor
    fontsize = Item.defaultfontsize
    textcolor = Item.textcolor
    
    # BaseType: tier    
    CurrencyBases = {
        '"Orb of Transmutation"': 1,
        '"Orb of Augmentation"': 1,
        '"Orb of Alteration"': 1,
        '"Orb of Chance"': 1,
        '"Orb of Alchemy"': 2,
        '"Chaos Orb"': 2,
        '"Orb of Scouring"': 2,
        '"Vaal Orb"': 2,
        '"Blessed Orb"': 2,
        '"Regal Orb"': 2,
        '"Exalted Orb"': 3,
        '"Divine Orb"': 3,
        '"Eternal Orb"': 3,
        '"Mirror of Kalandra"': 3,
        '"Armourer\'s Scrap"': 0,
        '"Blacksmith\'s Whetstone"': 0,
        '"Cartographer\'s Chisel"': 2,
        '"Glassblower\'s Bauble"': 2,
        '"Gemcutter\'s Prism"': 2,
        '"Chromatic Orb"': 1,
        '"Jeweller\'s Orb"': 1,
        '"Orb of Fusing"': 2,
        '"Orb of Regret"': 2,
        '"Portal Scroll"': 0,
        '"Scroll of Wisdom"': 0,
        '"Scroll Fragment"': 0,
        '"Perandus Coin"': 4,
        }
        
    CurrencyColors = {
        #Tier: (background, border, fontsize, textcolor, alertsound)
        0: (backgroundcolor, "0 0 0", Item.mediumfontsize, "170 158 130"),
        1: (backgroundcolor, "170 158 130", fontsize, "170 158 130"),
        2: (backgroundcolor, "255 0 0 200", 39, "255 0 0"),
        3: ("255 0 0 200", Item.Colors.get('Crafting')[1], fontsize, "170 158 130"),
        4: (backgroundcolor, "55 111 94", fontsize, "55 111 94"),
        }

class Gems(Item):

    backgroundcolor = Item.backgroundcolor
    bordercolor = Item.bordercolor
    fontsize = Item.defaultfontsize
    textcolor = Item.textcolor
        
    # Skill Gems: Highlight particularly valuable ones, then by quality and active/support probably just a list
    ValuableSkillGems = {
        '"Spell Echo"': ("need anything here?"),
        'Multistrike': ("sda")
        }
        
    GemColors = {
    #'type of gem': (background, border, fontsize, textsize)
        'Valuable': (backgroundcolor, "27 162 155", fontsize, "47 182 175"),
        'Quality': (backgroundcolor, "27 162 155", fontsize, "27 162 155"),
        'Active': (backgroundcolor, "27 162 155", fontsize, "27 162 155"),
        'Support': (backgroundcolor, "27 162 155", fontsize, "27 162 155")
        }
    
class Jewels(Item):
    backgroundcolor = Item.backgroundcolor
    bordercolor = Item.bordercolor
    fontsize = Item.defaultfontsize
    textcolor = Item.textcolor

class Maps(Item):
    backgroundcolor = Item.backgroundcolor
    bordercolor = Item.bordercolor
    fontsize = Item.defaultfontsize
    textcolor = Item.textcolor
    
    MapColors = {
    # Tier: (background, border, fontsize, textcolor)
        71: ("120 120 120", "236 255 0", fontsize, "68-70textcolor"),
        75: ("140 140 140", "0 255 102", fontsize + 1, "71-74textcolor"),
        78: ("160 160 160", "0 0 255", fontsize + 2, "75-77textcolot"),
        81: ("180 180 180", "255 0 249", fontsize + 3, "78-80textcolor"),
        100: ("200 200 200", "255 0 0", fontsize + 4, "81+textcolor")
        }

    
##############################################################################
 
# Open With Super Rare/Important Items

def OpeningGenerator():
    print '''Show
    Class "Hideout Doodads" Microtransactions "Quest Items"\nShow
    Class "Fishing Rod"
    SetTextColor 255 0 0
    SetFontSize 45
    SetBackgroundColor 255 255 255'''

# 5 or 6 Link Same for all Items and rarities so doesn't need any iteration.

def LinkedGenerator():

    rarity = Item.Rarity.keys()
        
    for rarity in rarity:
        if rarity == 'Unique':
            variables = Item.Rarity.get(rarity)
            print '''Show
    Rarity %s
    LinkedSockets 6
    SetBackgroundColor %s
    SetBorderColor %s
    SetFontSize %d
    PlayAlertSound %s
    ''' % (rarity, 
           Item.Rarity.get(rarity)[0], 
           Item.Rarity.get(rarity)[1], 
           Item.Colors.get('SixLink')[2],
           Item.Colors.get('SixLink')[4],
           )
            print '''Show
    Rarity %s
    LinkedSockets 5
    SetBackgroundColor %s
    SetBorderColor %s
    SetFontSize %d
    ''' % (rarity, 
           Item.Rarity.get(rarity)[0], 
           Item.Rarity.get(rarity)[1], 
           Item.Colors.get('FiveLink')[2]
           )
    
        else:
            pass
    
    print '''Show
    LinkedSockets 6
    SetBackgroundColor %s
    SetBorderColor %s
    SetFontSize %d
    ''' % (Item.Colors.get('SixLink')[0], 
           Item.Colors.get('SixLink')[1], 
           Item.Colors.get('SixLink')[2]
           )
    print '''Show
    LinkedSockets 5
    SetBackgroundColor %s
    SetBorderColor %s
    SetFontSize %d
    ''' % (Item.Colors.get('FiveLink')[0], 
           Item.Colors.get('FiveLink')[1], 
           Item.Colors.get('FiveLink')[2])

# Highlight Gems based on Support and Active+DropLevel

def GemGenerator():
    
    ValuableSkills = Gems.ValuableSkillGems.keys()
    valuable = Gems.GemColors.get('Valuable')
    quality = Gems.GemColors.get('Quality')
    active = Gems.GemColors.get('Active')
    support = Gems.GemColors.get('Support')
    
    for gem in ValuableSkills:
        
        print '''Show
    BaseType %s
    SetBackgroundColor %s
    SetBorderColor %s
    SetFontSize %d
    SetTextColor %s
    ''' % (gem, valuable[0], valuable[1], valuable[2], valuable[3])
    
    print '''Show
    Class Gem
    Quality > 0
    SetBackgroundColor %s
    SetBorderColor %s
    SetFontSize %d
    ''' % (quality[0], quality[1], quality[2])
    
    print'''Show
    Class Active
    SetBackgroundColor %s
    SetBorderColor %s
    SetFontSize %d\nShow
    Class Support
    SetBackgroundColor %s
    SetBorderColor %s
    SetFontSize %d
    ''' % (active[0], active[1], active[2], 
           support[0], support[1], support[2])
    
# Highlight Currencies based on rarity
    
def CurrencyGenerator():
    currency = Currency.CurrencyBases.keys()
    for currency in currency: 
        tier = Currency.CurrencyBases.get(currency)
        colors = Currency.CurrencyColors.get(tier)
        print'''Show
    BaseType %s
    SetBackgroundColor %s
    SetBorderColor %s
    SetFontSize %d
    SetTextColor %s
    ''' % (currency, colors[0], colors[1], colors[2], colors[3])
    
    ###Current Divination Card solution
    divcolors = Currency.CurrencyColors.get(1)
    print '''Show
    Class %s
    SetBackgroundColor %s
    SetBorderColor %s
    SetFontSize %d
    SetTextColor %s
    ''' % ('"Divination Card"', colors[0], colors[1], colors[2], colors[3])

# Highlight Jewels Based on Rarity

def JewelGenerator():

    rarity = Jewels.Rarity.keys()
    
    for rarity in rarity:
        
        if rarity == 'Normal':
            pass
        elif rarity == 'Unique':
            pass
        else:
            print '''Show
    Class Jewel
    Rarity %s
    SetBackgroundColor %s
    SetBorderColor %s
    SetFontSize %d
    ''' % (rarity,
           Jewels.Highlights.get(rarity)[0],
           Jewels.Highlights.get(rarity)[1], 
           Jewels.Highlights.get(rarity)[2]
           )
 
def UniqueGenerator():
    rarity = Item.Rarity.keys()
    for rarity in rarity:
        if rarity == 'Unique':
            print '''Show
    Rarity %s
    SetBackgroundColor %s
    SetBorderColor %s
    SetFontSize %d
    SetTextColor %s
    ''' % (rarity,
           Item.Rarity.get(rarity)[0],
           Item.Rarity.get(rarity)[1],
           Item.Rarity.get(rarity)[2],
           Item.Rarity.get(rarity)[3]
           )
        else:
            pass
 
# Highlight Maps, based on droplevel or basetype???

def MapGenerator():
    
    tiers = Maps.MapColors.keys()  # Gets the Tiers,
    tiers.sort(key=int) # Orders the tiers so that rules are generated in the order necessary for correct application
    
    for tier in tiers:
        
        print '''Show
    Class Map
    DropLevel < %s
    SetBackgroundColor %s
    SetBorderColor %s
    SetFontSize %d
    ''' % (tier,
           Maps.MapColors.get(tier)[0],
           Maps.MapColors.get(tier)[1],
           Maps.MapColors.get(tier)[2]
           )
    
def TopTierRegalRareGenerator():

    basetypes = Item.TopTierWeapons + Item.TopTierArmour
    
    for basetype in basetypes:
        print '''Show
    Rarity %s
    BaseType %s
    ItemLevel >= %d
    SetBackgroundColor %s
    SetBorderColor %s
    SetFontSize %d
    SetTextColor %s
    ''' % ('Rare',
           basetype,
           75, 
           Item.Colors.get('TopTier')[0],
           Item.Colors.get('Regal')[1],
           Item.Colors.get('TopTier')[2],
           Item.Highlights.get('Rare')[3]
           )
               
def TopTierChaosRareGenerator():

    basetypes = Item.TopTierWeapons + Item.TopTierArmour
    
    for basetype in basetypes:
        print '''Show
    Rarity %s
    BaseType %s
    ItemLevel >= %d
    SetBackgroundColor %s
    SetBorderColor %s
    SetFontSize %d
    SetTextColor %s
    ''' % ('Rare',
           basetype,
           60, 
           Item.Colors.get('TopTier')[0],
           Item.Colors.get('Chaos')[1],
           Item.Colors.get('TopTier')[2],
           Item.Highlights.get('Rare')[3]
           )
            
def TopTierItemsGenerator():

    basetypes = Item.TopTierWeapons + Item.TopTierArmour
    for basetype in basetypes:
        print '''Show
    BaseType %s
    ItemLevel >= 84
    SetBackgroundColor %s
    SetBorderColor %s
    SetFontSize %d
    ''' % (basetype,
           Item.Colors.get('TopTier')[0],
           Item.Colors.get('TopTier')[1],
           Item.Colors.get('TopTier')[2]
           )
           
    for basetype in Item.TopTierFlasks:
        print '''Show
    BaseType %s
    SetBackgroundColor %s
    SetBorderColor %s
    SetFontSize %d
    ''' % (basetype,
           Item.Colors.get('TopTier')[0],
           Item.Colors.get('TopTier')[1],
           Item.Colors.get('TopTier')[2]
           )
                   
def RareRegalSixSocketGenerator():

    print '''Show
    Rarity %s
    ItemLevel >= %d
    Sockets 6
    SetBackgroundColor %s
    SetBorderColor %s
    SetFontSize %d
    ''' % ('Rare',
         75,
         Item.Colors.get('Crafting')[0],
         Item.Colors.get('Regal')[1],
         Item.Colors.get('Regal')[2]
         )

def RareRegalChromaticGenerator():
    print '''Show
    Rarity %s
    ItemLevel >= %d
    SocketGroup %s
    SetBackgroundColor %s
    SetBorderColor %s
    SetFontSize %d
    ''' % ('Rare',
         75,
         'RGB',
         Item.Colors.get('Crafting')[0],
         Item.Colors.get('Regal')[1],
         Item.Colors.get('Regal')[2]
         )

def RareChaosSixSocketGenerator():
    print '''Show
    Rarity %s
    ItemLevel >= %d
    Sockets 6
    SetBackgroundColor %s
    SetBorderColor %s
    SetFontSize %d
    ''' % ('Rare',
         60,
         Item.Colors.get('Crafting')[0],
         Item.Colors.get('Chaos')[1],
         Item.Colors.get('Chaos')[2]
         )

def RareChaosChromaticGenerator():
    print '''Show
    Rarity %s
    ItemLevel >= %d
    SocketGroup %s
    SetBackgroundColor %s
    SetBorderColor %s
    SetFontSize %d
    ''' % ('Rare',
         60,
         'RGB',
         Item.Colors.get('Crafting')[0],
         Item.Colors.get('Chaos')[1],
         Item.Colors.get('Chaos')[2]
         )

def RareRegalGenerator():
    print '''Show
    Rarity %s
    ItemLevel >= %d
    SetBackgroundColor %s
    SetBorderColor %s
    SetFontSize %d
    ''' % ('Rare',
           75,
           Item.Colors.get('Regal')[0],
           Item.Colors.get('Regal')[1],
           Item.Colors.get('Regal')[2]
           )

def RareChaosGenerator():
    print '''Show
    Rarity %s
    ItemLevel >= %d
    SetBackgroundColor %s
    SetBorderColor %s
    SetFontSize %d
    ''' % ('Rare',
           60,
           Item.Colors.get('Chaos')[0],
           Item.Colors.get('Chaos')[1],
           Item.Colors.get('Chaos')[2]
           )

def ChromaticItemGenerator():

    ItemClasses = Item.ItemClasses + Item.NoDropLevelItemClasses

    for ItemClass in ItemClasses:
        basetype = ItemClass.keys()
        for basetype in basetype:
        
            Chromatic = ItemClass.get(basetype)[3]
            
            if Chromatic == 1:
            
                print '''Show
    BaseType %s
    SocketGroup %s
    SetBackgroundColor %s
    SetBorderColor %s
    SetFontSize %d
    ''' % (basetype, 'RGB',
           Item.Colors.get('Crafting')[0],
           Item.Colors.get('Crafting')[1],
           Item.Colors.get('Crafting')[2]
           )
           
            else:
                pass
           
def SixSocketGenerator():
    print '''Show
    Sockets 6
    SetBackgroundColor %s
    SetBorderColor %s
    SetFontSize %d
    ''' % (Item.Colors.get('Crafting')[0],
           Item.Colors.get('Crafting')[1],
           Item.Colors.get('Crafting')[2]
            )

def ChiselRecipeGenerator():
    print '''Show
    BaseType %s
    Rarity %s
    SetBackgroundColor %s
    SetBorderColor %s
    SetFontSize %d
    ''' % ('"Stone Hammer" "Rock Breaker" Gavel',
           'Normal',
           Item.Colors.get('Crafting')[0],
           Item.Colors.get('Crafting')[1],
           Item.Colors.get('Crafting')[2]
           )

def TwentyQualityNormalGenerator():
    print '''Show
    Rarity %s
    Quality %d
    SetBackgroundColor %s
    SetBorderColor %s
    SetFontSize %d
    ''' % ('Normal',
           20,
           Item.Colors.get('Crafting')[0],
           Item.Colors.get('Crafting')[1],
           Item.Colors.get('Crafting')[2]
           )

def ItemLevelGenerator():
    
    ItemClasses = Item.ItemClasses
    
    for ItemClass in ItemClasses:
    
        basetype = ItemClass.keys()
        
        for basetype in basetype:
            
            nexttier = ItemClass.get(basetype)[1]
            obsolete = ItemClass.get(basetype)[2]
            rarity = Item.Rarity.keys()
            
            for rarity in rarity:
                
################################################################                
                if rarity == 'Rare':
                    print '''Show
    Rarity %s
    BaseType %s
    ItemLevel < %d
    SetBackgroundColor %s
    SetBorderColor %s
    SetFontSize %d
    SetTextColor %s
    ''' % (rarity, basetype, nexttier, 
           Item.Colors.get('CurrentTier')[0],
           Item.Colors.get('CurrentTier')[1],
           Item.Highlights.get(rarity)[2],
           Item.Highlights.get(rarity)[3]
           )
                    print '''Show
    Rarity %s
    BaseType %s
    ItemLevel >= %d
    ItemLevel < %d
    SetBackgroundColor %s
    SetBorderColor %s
    SetFontSize %d
    SetTextColor %s
    ''' % (rarity, basetype, nexttier, obsolete,
           Item.Colors.get('SecondTier')[0],
           Item.Colors.get('SecondTier')[1],
           Item.Rarity.get(rarity)[2],
           Item.Rarity.get(rarity)[3]
           )
                    print '''Show
    Rarity %s
    BaseType %s
    ItemLevel >= %d
    SetBackgroundColor %s
    SetBorderColor %s
    SetFontSize %d
    SetTextColor %s
    ''' % (rarity, basetype, obsolete,
           Item.Colors.get('ObsoleteTier')[0],
           Item.Colors.get('ObsoleteTier')[1],
           Item.Rarity.get(rarity)[2],
           Item.Rarity.get(rarity)[3]
           )
#######################################################           
                elif rarity == 'Magic':
                    
                    print '''Show
    Rarity %s
    BaseType %s
    ItemLevel < %d
    SetBackgroundColor %s
    SetBorderColor %s
    SetFontSize %d
    SetTextColor %s
    ''' % (rarity, basetype, nexttier, 
           Item.Colors.get('CurrentTier')[0],
           Item.Colors.get('CurrentTier')[1],
           Item.Highlights.get(rarity)[2],
           Item.Highlights.get(rarity)[3]
           )
                    print '''Show
    Rarity %s
    BaseType %s
    ItemLevel >= %d
    ItemLevel < %d
    SetBackgroundColor %s
    SetBorderColor %s
    SetFontSize %d
    SetTextColor %s
    ''' % (rarity, basetype, nexttier, obsolete,
           Item.Colors.get('SecondTier')[0],
           Item.Colors.get('SecondTier')[1],
           Item.Rarity.get(rarity)[2],
           Item.Rarity.get(rarity)[3]
           )
                    print '''Hide
    Rarity %s
    BaseType %s
    ItemLevel >= %d
    SetBackgroundColor %s
    SetBorderColor %s
    SetFontSize %d
    SetTextColor %s
    ''' % (rarity, basetype, obsolete,
           Item.Colors.get('ObsoleteTier')[0],
           Item.Colors.get('ObsoleteTier')[1],
           Item.Lowlights.get(rarity)[2],
           Item.Lowlights.get(rarity)[3]
           )
##############################################################        
                elif rarity == 'Normal':
                   
                    print '''Show
    Rarity %s
    BaseType %s
    ItemLevel < %d
    SetBackgroundColor %s
    SetBorderColor %s
    SetFontSize %d
    SetTextColor %s
    ''' % (rarity, basetype, nexttier, 
           Item.Rarity.get(rarity)[0],
           Item.Rarity.get(rarity)[1],
           Item.Rarity.get(rarity)[2],
           Item.Rarity.get(rarity)[3]
           )
                    print '''Hide
    Rarity %s
    BaseType %s
    ItemLevel >= %d
    ItemLevel < %d
    SetBackgroundColor %s
    SetBorderColor %s
    SetFontSize %d
    SetTextColor %s
    ''' % (rarity, basetype, nexttier, obsolete,
           Item.Rarity.get(rarity)[0],
           Item.Rarity.get(rarity)[1],
           Item.Lowlights.get(rarity)[2],
           Item.Rarity.get(rarity)[3]
           )
                    print '''Hide
    Rarity %s
    BaseType %s
    ItemLevel >= %d
    SetBackgroundColor %s
    SetBorderColor %s
    SetFontSize %d
    SetTextColor %s
    ''' % (rarity, basetype, obsolete,
           Item.Colors.get('ObsoleteTier')[0],
           Item.Colors.get('ObsoleteTier')[1],
           Item.Lowlights.get(rarity)[2],
           Item.Lowlights.get(rarity)[3]
           )
        
                else:
                    pass

def AlchableJewelleryGenerator():
    print '''Show
    BaseType Ring Belt Amulet
    Rarity Normal
    ItemLevel >= 75
    SetBackgroundColor %s
    SetBorderColor %s
    SetFontSize %d
    SetTextColor %s
    ''' % (Item.Colors.get('Crafting')[0],
           Item.Colors.get('Regal')[1],
           Item.Colors.get('Regal')[2],
           Item.Highlights.get('Normal')[3]
           )

def JewelleryGenerator():
    # Find a way to print list of basetypes in acceptable syntax to cut down on blocks.
    for JewelleryClass in Item.JewelleryClasses:
    
        for basetype in JewelleryClass:
            if basetype in Item.ValuableJewellery:
                print '''Show
    BaseType %s
    ''' % basetype
            else:
                print '''Hide
    BaseType %s
    ''' % basetype
           
def FlaskTierGenerator():
    
    basetype = Item.Flasks.keys()
    
    for basetype in basetype:
        
        nexttier = Item.Flasks.get(basetype)[1]
        obsolete = Item.Flasks.get(basetype)[2]
        
        print '''Show
    BaseType %s
    ItemLevel < %d
    SetBackgroundColor %s
    SetBorderColor %s
    SetFontSize %d
    ''' % (basetype, nexttier,
           Item.Colors.get('CurrentTier')[0],
           Item.Colors.get('CurrentTier')[1],
           Item.Colors.get('CurrentTier')[2]
           )
        print '''Show
    BaseType %s
    ItemLevel >= %d
    ItemLevel < %d
    SetBackgroundColor %s
    SetBorderColor %s
    SetFontSize %d
    ''' % (basetype, nexttier, obsolete,
           Item.Colors.get('SecondTier')[0],
           Item.Colors.get('SecondTier')[1],
           Item.Colors.get('SecondTier')[2]
           )
        print ''' Show
    BaseType %s
    ItemLevel >= %d
    SetBackgroundColor %s
    SetBorderColor %s
    SetFontSize %d
    ''' % (basetype, obsolete,
           Item.Colors.get('ObsoleteTier')[0],
           Item.Colors.get('ObsoleteTier')[1],
           Item.Colors.get('ObsoleteTier')[2]
           )

def LeftOverGenerator():
    print '''Show
    SetFontSize 42
    SetBackgroundColor 0 0 0 255
    SetBorderColor 255 255 255 255
    SetTextColor 255 255 255 255
    '''

def QualityFlaskGenerator():
    print '''Show
    Class Flask
    Quality >= %d
    SetBackgroundColor %s
    SetBorderColor %s
    ''' % (5,
           Item.Colors.get('Crafting')[0],
           Item.Colors.get('Crafting')[1]
           )
           
def UtilityFlaskGenerator():
    Flasks = Item.UtilityFlasks.keys()
    for flask in Flasks:
        print '''Show
    BaseType %s
    SetBackgroundColor %s
    SetBorderColor %s
    ''' % (flask,
           Item.Colors.get('Flasks')[0],
           Item.Colors.get('Flasks')[1]
           )
    
def MaelstromStaffWorkaround():
    staff = 'Stave'
    droplevel = 64
    nexttier = 66
    obsolete = 68
    rarity = Item.Rarity.keys()
    for rarity in rarity:
        if rarity == 'Rare':
            
            print '''Show
    Rarity %s
    Class %s
    DropLevel %d
    ItemLevel < %d
    SetBackgroundColor %s
    SetBorderColor %s
    SetFontSize %d
    SetTextColor %s
    ''' % (rarity, staff, droplevel, nexttier, 
           Item.Colors.get('CurrentTier')[0],
           Item.Colors.get('CurrentTier')[1],
           Item.Highlights.get(rarity)[2],
           Item.Highlights.get(rarity)[3]
           )
            print '''Show
    Rarity %s
    Class %s
    DropLevel %d
    ItemLevel >= %d
    ItemLevel < %d
    SetBackgroundColor %s
    SetBorderColor %s
    SetFontSize %d
    SetTextColor %s
    ''' % (rarity, staff, droplevel, nexttier, obsolete,
           Item.Colors.get('SecondTier')[0],
           Item.Colors.get('SecondTier')[1],
           Item.Rarity.get(rarity)[2],
           Item.Rarity.get(rarity)[3]
           )
            print '''Show
    Rarity %s
    Class %s
    DropLevel %d
    ItemLevel >= %d
    SetBackgroundColor %s
    SetBorderColor %s
    SetFontSize %d
    SetTextColor %s
    ''' % (rarity, staff, droplevel, obsolete,
           Item.Colors.get('ObsoleteTier')[0],
           Item.Colors.get('ObsoleteTier')[1],
           Item.Rarity.get(rarity)[2],
           Item.Rarity.get(rarity)[3]
           )
            
        elif rarity == 'Magic':
            basecolors = Item.Rarity.get(rarity)
            print '''Show
    Rarity %s
    Class %s
    DropLevel %d
    ItemLevel < %d
    SetBackgroundColor %s
    SetBorderColor %s
    SetFontSize %d
    SetTextColor %s
    ''' % (rarity, staff, droplevel, nexttier, 
           Item.Colors.get('CurrentTier')[0],
           Item.Colors.get('CurrentTier')[1],
           Item.Highlights.get(rarity)[2],
           Item.Highlights.get(rarity)[3]
           )
            print '''Show
    Rarity %s
    Class %s
    DropLevel %d
    ItemLevel >= %d
    ItemLevel < %d
    SetBackgroundColor %s
    SetBorderColor %s
    SetFontSize %d
    SetTextColor %s
    ''' % (rarity, staff, droplevel, nexttier, obsolete,
           Item.Colors.get('CurrentTier')[0],
           Item.Colors.get('CurrentTier')[1],
           Item.Rarity.get(rarity)[2],
           Item.Rarity.get(rarity)[3]
           )
            print '''Show
    Rarity %s
    Class %s
    DropLevel %d
    ItemLevel >= %d
    SetBackgroundColor %s
    SetBorderColor %s
    SetFontSize %d
    SetTextColor %s
    ''' % (rarity, staff, droplevel, obsolete,
           Item.Colors.get('CurrentTier')[0],
           Item.Colors.get('CurrentTier')[1],
           Item.Lowlights.get(rarity)[2],
           Item.Lowlights.get(rarity)[3]
           )
        
        elif rarity == 'Normal':
            basecolors = Item.Rarity.get(rarity)
            print '''Show
    Rarity %s
    Class %s
    DropLevel %d
    ItemLevel < %d
    SetBackgroundColor %s
    SetBorderColor %s
    SetFontSize %d
    SetTextColor %s
    ''' % (rarity, staff, droplevel, nexttier, 
           Item.Colors.get('CurrentTier')[0],
           Item.Colors.get('CurrentTier')[1],
           Item.Highlights.get(rarity)[2],
           Item.Rarity.get(rarity)[3]
           )
            print '''Hide
    Rarity %s
    Class %s
    DropLevel %d
    ItemLevel >= %d
    ItemLevel < %d
    SetBackgroundColor %s
    SetBorderColor %s
    SetFontSize %d
    SetTextColor %s
    ''' % (rarity, staff, droplevel, nexttier, obsolete,
           Item.Colors.get('CurrentTier')[0],
           Item.Colors.get('CurrentTier')[1],
           Item.Rarity.get(rarity)[2],
           Item.Rarity.get(rarity)[3]
           )
            print '''Hide
    Rarity %s
    Class %s
    DropLevel %d
    ItemLevel >= %d
    SetBackgroundColor %s
    SetBorderColor %s
    SetFontSize %d
    SetTextColor %s
    ''' % (rarity, staff, droplevel, obsolete,
           Item.Colors.get('CurrentTier')[0],
           Item.Colors.get('CurrentTier')[1],
           Item.Lowlights.get(rarity)[2],
           Item.Lowlights.get(rarity)[3]
           )
        
        else:
            pass
            
def NoDropLevelItemClassesGenerator():
    
    ItemClasses = Item.NoDropLevelItemClasses
    
    for ItemClass in ItemClasses:
            
        basetype = ItemClass.keys()
        for basetype in basetype:
            rarity = Item.Rarity.keys()
            for rarity in rarity:
        
                basecolors = Item.Rarity.get(rarity)
                highlights = Item.Highlights.get(rarity)
                lowlights = Item.Lowlights.get(rarity)
            
                if rarity == 'Rare':
            
                    print '''Show
    Rarity %s
    BaseType %s
    LinkedSockets 3
    SetBackgroundColor %s
    SetBorderColor %s
    SetFontSize %d
    SetTextColor %s
    ''' % (rarity, basetype,
            Item.Highlights.get(rarity)[0],
            Item.Highlights.get(rarity)[1],
            Item.Highlights.get(rarity)[2],
            Item.Highlights.get(rarity)[3]
            )
                    print '''Show
    Rarity %s
    BaseType %s
    SetBackgroundColor %s
    SetBorderColor %s
    SetFontSize %d
    SetTextColor %s
    ''' % (rarity, basetype,
            Item.Rarity.get(rarity)[0],
            Item.Rarity.get(rarity)[1],
            Item.Rarity.get(rarity)[2],
            Item.Rarity.get(rarity)[3]
            )
    
            
                elif rarity == 'Magic':
                
                    print '''Show
    Rarity %s
    BaseType %s
    LinkedSockets 3
    SetBackgroundColor %s
    SetBorderColor %s
    SetFontSize %d
    SetTextColor %s
    ''' % (rarity, basetype,
            Item.Highlights.get(rarity)[0],
            Item.Highlights.get(rarity)[1],
            Item.Highlights.get(rarity)[2],
            Item.Highlights.get(rarity)[3]
            )
                    print '''Show
    Rarity %s
    BaseType %s
    SetBackgroundColor %s
    SetBorderColor %s
    SetFontSize %d
    SetTextColor %s
    ''' % (rarity, basetype,
            Item.Rarity.get(rarity)[0],
            Item.Rarity.get(rarity)[1],
            Item.Rarity.get(rarity)[2],
            Item.Rarity.get(rarity)[3]
            )
            
                elif rarity == 'Normal':
                    print '''Show
    Rarity %s
    BaseType %s
    LinkedSockets 3
    SetBackgroundColor %s
    SetBorderColor %s
    SetFontSize %d
    SetTextColor %s
    ''' % (rarity, basetype,
            Item.Highlights.get(rarity)[0],
            Item.Highlights.get(rarity)[1],
            Item.Rarity.get(rarity)[2],
            Item.Rarity.get(rarity)[3]
            )
                    print '''Hide
    Rarity %s
    BaseType %s
    SetBackgroundColor %s
    SetBorderColor %s
    SetFontSize %d
    SetTextColor %s
    ''' % (rarity, basetype,
            Item.Lowlights.get(rarity)[0],
            Item.Lowlights.get(rarity)[1],
            Item.Lowlights.get(rarity)[2],
            Item.Lowlights.get(rarity)[3]
            )
            
                else:
                    pass
           
##############################################################################
    
def Generator():
    OpeningGenerator()
    LinkedGenerator()
    CurrencyGenerator()
    UniqueGenerator()
    GemGenerator()
    JewelGenerator()
    MapGenerator()    
    TopTierRegalRareGenerator()    
    TopTierChaosRareGenerator()
    TopTierItemsGenerator()
    RareRegalSixSocketGenerator()
    RareRegalChromaticGenerator()
    RareChaosSixSocketGenerator()
    RareChaosChromaticGenerator()
    RareRegalGenerator()
    RareChaosGenerator()
    AlchableJewelleryGenerator()
    ChromaticItemGenerator()
    SixSocketGenerator()
    ChiselRecipeGenerator()
    #TwentyQualityNormalGenerator()
    QualityFlaskGenerator()
    ItemLevelGenerator()
    MaelstromStaffWorkaround()
    FlaskTierGenerator()
    JewelleryGenerator()
    UtilityFlaskGenerator()
    LeftOverGenerator()
        
 
Generator()