from random import randint,random,shuffle,choice
# from wizard import Wizard
# from rogue import Rogue
# from knight import Knight

import os
def cls():
    os.system('cls' if os.name=='nt' else 'clear')
cls()
class Colors():
    LIGHT_GRAY = "\033[0;37m"
    RED = "\033[0;31m"
    BLUE = "\033[0;34m"
    DARK_GRAY = "\033[1;30m"
    LIGHT_RED = "\033[1;31m"
    END = "\033[0m"
    LIGHT_GREEN = "\033[1;32m"
    BLACK = "\033[0;30m"
    YELLOW = "\033[1;33m"
    LIGHT_PURPLE = "\033[1;35m"
    PURPLE = "\033[0;35m"

class Status():
    def __init__(self,effect,duration,amount,chance):
        self.effect=effect
        self.duration=duration
        self.amount=amount
        self.chance=chance

class GameField():
    def __init__(self, weather, terrain):
        self.weather = weather
        self.terrain = terrain

    def calculate_accuracy(self, ability_type):
        accuracy = 1.0 # Default accuracy

        if self.weather == "Rainy":
            if ability_type == "attack":
                accuracy *= 0.8 # Reduce accuracy for attacks in rainy weather
        elif self.weather == "Sunny":
            if ability_type == "special":
                accuracy *= 1.2 # Increase accuracy for special abilities in sunny weather

        if self.terrain == "Mountain":
            if ability_type == "attack":
                accuracy *= 0.7 # Reduce accuracy for attacks on mountain terrain
        elif self.terrain == "Plains":
            if ability_type == "attack":
                accuracy *= 1.2
            elif ability_type == "special":
                accuracy *= .8
        return accuracy


class Player():
    hp=50
    max_hp=50
    
    block=0
    starting_block=0 #player.status

    dam_mult=1

    mana=10
    max_mana=10
    mana_regen=0

    accuracy_mod=1
    can_attack=True

    def __init__(self,name):
        self.name=name
        self.abilities=[] 
        self.statuses=[]
        self.upgrades={"damage upgrade":0,"block upgrade":0,"max hp upgrade":0,"heal":0,"heal upgrade":0,"status duration upgrade":0,"status upgrade":0,"status duration upgrade":0,"mana regen upgrade":0}

    def add_ability(self,ability):
        self.abilities.append(ability)
    
    def inflicted_with_status(self,status):
        # how to add the status duration upgrade to the statuses dictionary list
        # print(status)
        # print(f'{status.chance} acc mod {self.accuracy_mod} Random:{random()}')
        status_amount=len(self.statuses)
        if random()<status.chance*self.accuracy_mod:
            # print(status.effect)
            if(self.statuses):
                count=0
                if(status.effect=="shock"):
                    print(f'{self.name} was shocked and is unable to use an ability')
                    self.can_attack=False
                if(status.effect=="pierce"):
                    self.block=0
                    print(f'{self.name}\'s block was destroyed...\n')
                for e in self.statuses:
                    count+=1
                    if e.effect == status.effect:
                        e.amount+=status.amount+self.upgrades['status upgrade']
                        e.duration+=status.duration+self.upgrades['status duration upgrade']
                        print(f'{e.effect}: +{status.amount} Turns left: {e.duration}')
                        break
                    elif count==status_amount:
                        status.amount+=self.upgrades['status upgrade']
                        status.duration+=self.upgrades['status duration upgrade']
                        self.statuses.append(status)
                        print(f'Applied {status.amount} {e.effect} for {e.duration} turns\n')
            else:
                status.amount+=self.upgrades['status upgrade']
                status.duration+=self.upgrades['status duration upgrade']
                self.statuses.append(status)
                print(f'Applied {status.amount} {status.effect} for {status.duration} turns\n')
        else:
            if(status.effect):
                print(f'\n{Colors.RED}-------{status.effect} failed to apply-------{Colors.END}\n')


    def calculated_end_round_status_amount(self,target):
        # print("end of round status")
        # print(self.statuses)
        for e in self.statuses:
            if e.duration>0:#if statements for e.effect
                # amount_upgrade
                if e.effect=="burn":
                    self.hp=self.hp-e.amount
                    print(f'{self.name} was hurt by {e.effect} for {e.amount} damage ---------- {self.name} Hp: {self.hp}/{self.max_hp} {e.duration-1} turns left\n')
                elif e.effect=="regen":
                    total_regen=e.amount
                    if self.hp+total_regen>self.max_hp:
                        self.hp=self.max_hp
                    else:
                        self.hp+=total_regen
                if e.effect=="shock":
                        # print(f'{self.name} was shocked and is unable to use an ability')
                        self.can_attack=False
                if e.effect=="blind":
                    self.accuracy_mod*=.5
                e.duration-=1
            else:
                self.can_attack=True
                self.accuracy_mod=1


    def rand_heal(self):
        rando=randint(0,20)
        self.hp+=rando+self.upgrades["heal upgrade"]
        if(self.hp>self.max_hp):
            self.hp=self.max_hp
        print("\n")
        print("Healing for "+str(rando)+" HP"+str(self.upgrades["heal upgrade"])+" ------------- New Health: "+str(self.hp)+"/"+str(self.max_hp))

    def add_upgrade(self,upgrade_name,upgrade_amount):
        if(upgrade_name.lower() in self.upgrades):
            self.upgrades[upgrade_name.lower()]+=upgrade_amount
            if(upgrade_name.lower()=="max hp upgrade"):
                self.max_hp+=upgrade_amount
                self.hp+=upgrade_amount
            if(upgrade_name.lower()=="mana regen upgrade"):
                self.mana_regen+=upgrade_amount
            if(upgrade_name.lower()=="heal"):
                self.upgrades['heal']=0
                self.hp+=upgrade_amount+self.upgrades["heal upgrade"]
                print(f'Healed For {upgrade_amount}(+{self.upgrades["heal upgrade"]}) ------------ Current Health: {self.hp}/{self.max_hp}')
                if(self.hp>self.max_hp):
                    self.hp=self.max_hp
            
            
    def activate_ability(self,ability_name,target,game_field):
        #look for correct ability in ability list then type then do the thing 
        for ab in self.abilities:
            ab_name=ab.ability["name"]
            # print(self.name+" used "+ab_name)
            ab_type=ab.ability["type"]
            ab_damage=ab.ability["damage"]
            accuracy = game_field.calculate_accuracy(ab_type)
            if random() < accuracy and self.can_attack:
                if(ab_name.lower()==ability_name.lower()):
                    print(Colors.BLUE+self.name+" used "+ab_name+Colors.END+"\n")
                    if(ab_type=="attack"):
                        if self.can_set_dam_mult(ab): 
                            total_damage=(ab_damage+self.upgrades["damage upgrade"])*self.dam_mult
                            total_damage=round(total_damage)
                        else:
                            total_damage=(ab_damage+self.upgrades["damage upgrade"])
                        print("\n"+self.name+" did "+str(total_damage)+" (x"+str(self.dam_mult)+")"+" damage to "+target.name+", Shield blocked: "+str(target.block)+"  --------  " +target.name+ " HP: "+str(target.hp)+"/"+str(target.max_hp)+" -"+str(total_damage-target.block))
                        
                    if(ab_type=="defend"):
                        ab_block=ab.ability["block"]
                        total_block=ab_block+self.upgrades["block upgrade"]
                        self.block+=total_block
                        print(self.name+" Adding "+str(total_block)+" block,  Total Block: "+str(self.block))

                    if(ab_type=="special"):
                        ab_block=ab.ability["block"]
                        ab_health=ab.ability["health"]
                        total_block=ab_block+self.upgrades["block upgrade"]
                        if(ab_name.lower()=="shield throw"):
                            ab_damage=self.block
                            self.block=0
                        if self.can_set_dam_mult(ab): 
                            total_damage=(ab_damage+self.upgrades["damage upgrade"])*self.dam_mult
                            total_damage=round(total_damage)
                        else:
                            total_damage=(ab_damage+self.upgrades["damage upgrade"])
                        
                            

                        status_effect=ab.ability["status"]["effect"]
                        status_turns_left=ab.ability["status"]["turns left"] + self.upgrades['status duration upgrade']
                        status_amount=ab.ability["status"]["amount"] + self.upgrades['status upgrade']
                        status_chance=ab.ability["status"]["chance"] #POSSIBLY add a status chance upgrade
                        status=Status(status_effect,status_turns_left,status_amount,status_chance)

                        if status_effect.lower() in ["burn","blind","shock","weaken"]:
                            # for effect do something
                            target.inflicted_with_status(status) #append the status damage
                        else:
                            player.inflicted_with_status(status)
                            
                        if ab_block>0:
                            self.block=self.block+total_block
                        if(not total_damage-target.block<0):
                            target.hp=target.hp+target.block-total_damage
                            print(self.name+" did "+str(total_damage)+" (x"+str(self.dam_mult)+")"+" damage to "+target.name+", Shield blocked: "+str(target.block)+"  --------  " +target.name+ " HP: "+str(target.hp)+"/"+str(target.max_hp)+" -"+str(total_damage-target.block))   
                        if ab_health>0:# if ability has a health modifier then update your health
                            self.hp+=ab_health+self.upgrades["heal upgrade"]
                            if self.hp>self.max_hp:
                                self.hp=self.max_hp
                            print(f'{self.name} Healed for {ab_health}(+{self.upgrades["heal upgrade"]}) new hp {self.hp}/{self.max_hp}')
                    if self.mana+self.mana_regen+self.upgrades["mana regen upgrade"]>self.max_mana:
                        self.mana=self.max_mana
                        print(f'Mana Full {self.mana}/{self.max_mana} Mana Regen: {self.mana_regen+self.upgrades["mana regen upgrade"]}\n')
                    elif self.mana_regen>0:
                        self.mana+=self.mana_regen+self.upgrades["mana regen upgrade"]
                        print(f'{self.name} Regenerated {self.mana_regen+self.upgrades["mana regen upgrade"]} Mana ------> {self.mana}/{self.max_mana}\n')
                elif(ab==self.abilities[-1] and ab_name.lower()!=ability_name.lower()):
                    print("\n")
                    #print("You don't have an ability with that name.")
            elif(not self.can_attack):
                print(f"{self.name} Can't attack this turn")
            else:
                if((ab_type=='attack' or ab_type=='special') and ab_name.lower()==ability_name.lower()):
                    print(f'{Colors.BLUE}{self.name} Missed While Using {ab_name}{Colors.END}')
                    
            self.can_attack=True
    
    def activate_random_ability(self,target,game_field): #pass ability name and activate it
        shuffle(self.abilities)
        # print(self.abilities[0].ability["name"])
        self.activate_ability(self.abilities[0].ability["name"],target,game_field)
    
    def random_ability(self):
        shuffle(self.abilities)
        random_ability=self.abilities[0].ability["name"]
        return random_ability
        # print(f'{self.name} will use {random_ability}')
    
    def add_random_ability(self):
        abil_names=[ability.ability["name"].lower() for ability in self.abilities]
        random_ability=choice(Ability.all_ability_names)
        while True:
            if not random_ability in abil_names:
                new_abil=Ability(random_ability)
                self.add_ability(new_abil)
                print(f'{self.name} got a new ability: {new_abil.ability["name"]} ------- Description {new_abil.ability["description"]}')
                break
            
    def attack(self,enemy,damage_of_ability):
        enemy.hp = enemy.hp+enemy.block-damage_of_ability
        return "Opp new HP: "+str(enemy.hp)

    def print_hp_string(self):
        bars=20
        red=Colors.LIGHT_RED
        end=Colors.END
        green=Colors.LIGHT_GREEN
        black=Colors.BLACK
        yellow=Colors.YELLOW
        blue=Colors.BLUE
        

        remaining_health_symbol=red+'▓'+end
        lost_health_symbol=red+"░"+end
        if self.hp/self.max_hp>.7:
            remaining_health_symbol=green+'▓'+end
            lost_health_symbol=green+"░"+end
        elif self.hp/self.max_hp>.25:
            remaining_health_symbol=yellow+'▓'+end
            lost_health_symbol=yellow+"░"+end
        else:
            remaining_health_symbol=red+'▓'+end
            lost_health_symbol=red+"░"+end
        remaining_health_player=round(self.hp/self.max_hp * bars)
        lost_health_bars_player=bars-remaining_health_player
        statuses=""
        for e in self.statuses:
            statuses+=e.effect+" "+str(e.duration)
        
        print(f'{self.name} HP: {round(self.hp)}/{self.max_hp} Block: {self.block}')
        print(f'|{remaining_health_player*remaining_health_symbol}{lost_health_bars_player*lost_health_symbol}| \n')
        # print(f'|{remaining_mana_player*remaining_mana_symbol}{lost_mana_bars_player*lost_mana_symbol}|\n')

    
    def can_set_dam_mult(self,ability):
        self.dam_mult=1
        return False
    
    # give 3 Random abilities to choose from with different chances for each rarity
    def reward_ability_three(self):
        rarity_count = {"common": 0, "uncommon": 0, "epic": 0}
        self.abilites_to_choose_from=[]

        for _ in range(0, 3):
            random_rarity_decimal = random()
            if random_rarity_decimal <= 0.55:
                rarity_count["common"] += 1
                # print("common")
            elif random_rarity_decimal <= 0.86:               
                # print("uncommon")
                rarity_count["uncommon"] += 1
            elif random_rarity_decimal <= 1:
                # print("epic")
                rarity_count["epic"] += 1

        self.abilities_to_exclude = [ability.ability["name"].lower() for ability in self.abilities]
        reward_number=0
        self.show_new_ability_reward("common",rarity_count,reward_number,Ability.common_names)
        reward_number=rarity_count["common"]
        self.show_new_ability_reward("uncommon",rarity_count,reward_number,Ability.uncommon_names)
        reward_number+=rarity_count["uncommon"]
        self.show_new_ability_reward("epic",rarity_count,reward_number,Ability.epic_names)
        reward_number+=rarity_count["epic"]
        
    def show_new_ability_reward(self,rarity,rarity_count,reward_number,rarity_list_names):  
        are_new_ability=True
        if(rarity=="common"):
            col=Colors.LIGHT_GREEN
        elif(rarity=="uncommon"):
            col=Colors.BLUE
        elif(rarity=="epic"):
            col=Colors.LIGHT_PURPLE
        for e in range(rarity_count[rarity]):
            while True and are_new_ability:
                random_ability_name = choice(rarity_list_names)
                random_ability = Ability(random_ability_name)
                # print(random_ability_name)
                if not random_ability_name.lower() in self.abilities_to_exclude:
                    
                    print(f'{reward_number+(e+1)}. Name: {random_ability_name.capitalize()} --------- Rarity: {col}{rarity.upper()}{Colors.END} --------- Description: {random_ability.ability["description"]}')
                    self.abilities_to_exclude.append(random_ability_name.lower())
                    self.abilites_to_choose_from.append(random_ability)
                    # print(self.abilites_to_choose_from)
                    # print(self.abilities_to_exclude)
                    break
                else:
                    # print(self.abilities_to_exclude)
                    # Ability.common_names.remove(random_ability_name)
                    if len(self.abilities_to_exclude)+len(self.abilities) == len(rarity_list_names):
                        print(f'no more {rarity} abilities')
                        print(self.abilities_to_exclude)
                        print(rarity_list_names)
                        are_new_ability=False
                        break

class Wizard(Player):
    info="Wizards gain x1.5 Damage to special attacks, but they consume mana. They cannot use special attacks without having enough mana. Start with 1 mana regen per turn. Wizards always start with Tackle and Guard"
    class_upgrades=[{"name":"Mana Mult Upgrade","amount":.2}]
    def __init__(self, name):
        super().__init__(name)
        # self.health = health
        self.mana = 10
        self.max_mana=10
        self.mana_regen=1
        self.class_name="Wizard"
        self.add_ability(Ability("tackle"))
        # print(self.hp)
    
    def can_set_dam_mult(self,ability):
        mana_cost=ability.ability["mana cost"]
        name=ability.ability["name"]
        if self.mana>=mana_cost and mana_cost>0:
            self.mana-=mana_cost
            self.dam_mult=1.5
            print(f'{name} spent {mana_cost} Mana, Current Mana {self.mana}/{self.max_mana}')
            return True
        else:
            self.dam_mult=1
            return False

    def activate_ability(self, ability_name, target, game_field): #wizards method to update mana and do more damage from special attacks
        for ab in self.abilities:
            ab_name=ab.ability["name"]
            # print(self.name+" used "+ab_name)
            ab_type=ab.ability["type"]
            ab_damage=ab.ability["damage"]
            if ab_name.lower() in ["fireball","heal","hp sacrifice","thunderbolt","all in","hp regen","blind"]:
                ab_mana_cost=ab.ability["mana cost"]
            
            # accuracy = game_field.calculate_accuracy(ab_type)
            if ab_type=="special" and ab_mana_cost!=0:
                if self.mana >= ab_mana_cost:
                    # Subtract the mana cost from the wizard's current mana
                    self.mana -= ab_mana_cost
                    # Proceed with activating the ability
                    super().activate_ability(ability_name, target, game_field)
                else:
                    print("Not enough mana to use this ability")

            return super().activate_ability(ability_name, target, game_field)
    
    def print_hp_string(self):
        bars=20
        red=Colors.LIGHT_RED
        end=Colors.END
        green=Colors.LIGHT_GREEN
        black=Colors.BLACK
        yellow=Colors.YELLOW
        blue=Colors.BLUE
        remaining_mana_symbol=blue+'▓'+end
        lost_mana_symbol=blue+"░"+end

        remaining_health_symbol=red+'▓'+end
        lost_health_symbol=red+"░"+end
        if self.hp/self.max_hp>.7:
            remaining_health_symbol=green+'▓'+end
            lost_health_symbol=green+"░"+end
        elif self.hp/self.max_hp>.25:
            remaining_health_symbol=yellow+'▓'+end
            lost_health_symbol=yellow+"░"+end
        else:
            remaining_health_symbol=red+'▓'+end
            lost_health_symbol=red+"░"+end
        remaining_health_player=round(self.hp/self.max_hp * bars)
        lost_health_bars_player=bars-remaining_health_player
        remaining_mana_player=round(self.mana/self.max_mana * bars)
        lost_mana_bars_player=bars-remaining_mana_player
        print(f'{self.name} HP: {round(self.hp)}/{self.max_hp}    Mana: {self.mana}/{self.max_mana}     Block: {self.block}')
        print(f'|{remaining_health_player*remaining_health_symbol}{lost_health_bars_player*lost_health_symbol}| |{remaining_mana_player*remaining_mana_symbol}{lost_mana_bars_player*lost_mana_symbol}| \n')
        # print(f'|{remaining_mana_player*remaining_mana_symbol}{lost_mana_bars_player*lost_mana_symbol}|\n')


class Knight(Player): #if block is higher than 10 do double damage
    info="Knights have high base armor gain and always start with shield throw. Knights also do 2x damage when above 10 armor... NOT FINISHED"
    def __init__(self, name):
        super().__init__(name)
        # self.health = health
        self.class_name="Knight"
        self.max_mana=10
        self.mana = 10
        self.mana_regen=0
        self.add_ability(Ability("shield throw"))

    def activate_ability(self, ability_name, target, game_field):
        if(ability_name.lower()=="shield throw"):
            print('shield throw')
            print(f'{self.block}')
        super().activate_ability(ability_name,target,game_field)

class Rogue(Player): #
    info="Rogue's have high evasion, but low health. Rogues always start with sneak attack and blind. Rogues do 2x damage when target is blinded or shocked ... NOT FINISHED"
    def __init__(self, name):
        super().__init__(name)
        self.hp = self.hp/2
        self.max_hp = int(self.hp)
        # self.mana = 10
        # self.mana_regen=0
        # self.max_mana=10
        self.class_name="Rogue"
        # self.add_ability(Ability("sneak attack")) #does 2.5X damage when target is shocked or confused
        self.add_ability(Ability("blind"))
        
    


class Ability():
    all_ability_names=["slash","fireball","guard","hp sacrifice","uppercut","charge","shield bash","thunderbolt","heal","all in","hp regen","tackle","sneak attack","blind","shield throw"]
    common_names=["slash","fireball","guard","hp sacrifice","uppercut","tackle"]
    uncommon_names=["charge","shield bash","thunderbolt","heal","shield throw"]
    epic_names=["all in","hp regen"]

    # starting abilities common
    tackle={"name":"Tackle","type":"attack","block":0,"damage":5,"description":"A weak attack that deals 5 base damage (Wizard Only)","mana cost":0}
    sneak_attack={"name":"Sneak attack","type":"special","block":0,"damage":10,"description":"A starting special attack that deals 10 base damage, 2.5X damage if target is blinded or shocked (Rogue Only).","mana cost":0,"status":{"effect":"","turns left":0,"amount":0,"chance":0}}
    blind={"name":"Blind","type":"special","block":0,"damage":5,"description":"A special attack that deals 5 base damage and has a 25% chance to inflict blind: blinded character's accuracy is halved for 2 (base) turns .","mana cost":3,"status":{"effect":"blind","turns left":2,"amount":0,"chance":0.25}}

    slash={"name":"Slash","type":"attack","block":0,"damage":8,"description":"A basic attack that deals 8 base damage","mana cost":0}
    fireball={"name":"Fireball","type":"special","block":0,"health":0,"damage":10,"description":"A magic attack that deals 10 base damage and has a 50% chance to inflict burn: 2 base damage per turn to opponent, can stack","status":{"effect":"burn","turns left":3,"amount":2,"chance":0.5},"mana cost":3}
    guard={"name":"Guard","type":"defend","damage":0,"speed":2,"block":4,"description":"An ability that gives 4 block (goes away at the start of your turn)","mana cost":0}
    hp_sac={"name":"Hp sacrifice","type":"special","damage":15,"block":0,"health":-5,"description":"A special attack that sacrifices 5 hearts to deal 18 damage","status":{"effect":"","turns left":0,"amount":0,"chance":0},"mana cost":2}
    # reward abilities common
    uppercut={"name":"Uppercut","type":"attack","damage":15,"block":0,"description":"Uppercut that deals 15 damage","mana cost":0}
    # strenghten: next attack x1.5
    # reward abilities uncommon
    shield_throw={"name":"Shield throw","type":"special","damage":0,"block":0,"health":0,"description":"Throw your shield and do damage based on your block. All block is then removed","mana cost":0,"status":{"effect":"","turns left":0,"amount":0,"chance":0}}

    heal={"name":"Heal","type":"special","damage":0,"block":0,"health":7,"description":"An uncommon ability that heals you for 7 (base) hp","status":{"effect":"","turns left":0,"amount":0,"chance":1.00},"mana cost":5}
    charge={"name":"Charge","type":"attack","damage":12,"description":"An uncommon attack that deals 12 base damage","mana cost":0}
    shield_bash={"name":"Shield bash","type":"special","damage":10,"block":5,"health":0,"description":"An uncommon ability that deals 10 base damage and gives 5 base block","mana cost":0,"status":{"effect":"weaken","turns left":1,"amount":0.5,"chance":0.25}}
    thunderbolt={"name":"Thunderbolt","type":"special","damage":10,"block":0,"health":0,"description":"A magic attack that deals 10 base damage and has a 25'%' chance to stun for 1 round","mana cost":3,"status":{"effect":"shock","turns left":1,"amount":1,"chance":0.30}}
    pierce={"name":"Pierce","type":"special","damage":12,"block":0,"health":0,"description":"An uncommon ability that does 12 base damage and ignores block","mana cost":0,"status":{"effect":"pierce","turns left":0,"amount":0,"chance":1.00}}
    #reward abilities epic
    allIn={"name":"All in","type":"special", "damage":50,"block":0,"description":"An epic Ability that does 50 base damage, but only has 3 uses.", "usesLeft":3,"mana cost":4,"status":{"effect":"shock","turns left":1,"amount":1,"chance":0.5},"health":0}
    hpRegen={"name":"Hp regen","type":"special","block":0, "damage":0,"description":"An epic Ability that heals you for 5 base health for 3 turns.","mana cost":8,"status":{"effect":"regen","turns left":3,"amount":5,"chance":1},"health":0}

    # reward abilities legendary


    def __init__(self,ability):
        if(ability.lower()=="slash"):
            self.ability=self.slash
            self.default_ability=self.slash
        elif(ability.lower()=="fireball"):
            self.ability=self.fireball
            self.default_ability=self.fireball
        elif(ability.lower()=="guard"):
            self.ability=self.guard
            self.default_ability=self.guard
        elif(ability.lower()=="hp sacrifice"):
            self.ability=self.hp_sac
            self.default_ability=self.hp_sac
        elif(ability.lower()=="uppercut"):
            self.ability=self.uppercut
        elif(ability.lower()=="tackle"):
            self.ability=self.tackle
        elif(ability.lower()=="sneak attack"):
            self.ability=self.sneak_attack
        elif(ability.lower()=="blind"):
            self.ability=self.blind
        elif(ability.lower()=="pierce"):
            self.ability=self.pierce

        elif(ability.lower()=="charge"):
            self.ability=self.charge
        elif(ability.lower()=="shield throw"):
            self.ability=self.shield_throw
        elif(ability.lower()=="shield bash"):
            self.ability=self.shield_bash
        elif(ability.lower()=="thunderbolt"):
            self.ability=self.thunderbolt
        elif(ability.lower()=="heal"):
            self.ability=self.heal
        elif(ability.lower()=="all in" or ability.lower()=="allin"):
            self.ability=self.allIn
        elif(ability.lower()=="hp regen"):
            self.ability=self.hpRegen

        # print(self.ability)





field_conditions={"weather":["Rainy","Sunny"],"terrain":["Mountain","Plains"]}
while True:
    name_input=input("\nWelcome, Please Enter a Name: ")
    cls()
    if name_input.isalpha() and len(name_input)>0:
        name_input=name_input.capitalize()
        break
    else:
        print("Invalid input. Please enter a name with at least one letter.")

while True:
    cls()
    print("\nChoose your class:\n\n")
    print(f"1. Wizard: {Wizard.info}\n")
    print(f"2. Rogue: {Rogue.info}\n")
    print(f"3. Knight: {Knight.info}\n")

    class_choice = input("Enter the number of your chosen class: ")
    if class_choice=="1":
        player = Wizard(name_input)
        break
    elif class_choice=="2":
        player = Rogue(name_input)
        break
    elif class_choice=="3":
        player = Knight(name_input)
        break

# player=Player("Nick")

opp=Player("Opponent")
upgrades=[{"name":"Damage Upgrade","amount":2},{"name":"Damage Upgrade","amount":5},{"name":"Block Upgrade","amount":5},{"name":"Max Hp Upgrade","amount":10},{"name":"Block Upgrade","amount":3},{"name":"Max Hp Upgrade","amount":20},{"name":"Heal","amount":20},{"name":"Heal","amount":50},{"name":"Block Upgrade","amount":10},{"name":"Damage Upgrade","amount":8},{"name":"Heal Upgrade","amount":2},{"name":"Status Upgrade","amount":2},{"name":"Status Upgrade","amount":4},{"name":"mana regen upgrade","amount":2},{"name":"mana regen upgrade","amount":1}]
round_number=0
isPlaying=True
while isPlaying:
    cls()
    if Ability in player.abilities:
        for e in player.abilities:
            print(f'\n\n{player.name.capitalize()} starts with {e.ability["name"]}, Description: {e.ability["description"]}\n')
    
    print("=========================================================================================================================")
    print("Choose your default ability: ")
    act_ans=input(f'\n1.Slash--Description: {Ability.slash["description"]} \n\n2.Fireball--Description: {Ability.fireball["description"]}\n\n3.Hp Sacrifice--Description:  {Ability.hp_sac["description"]}\n\nEnter Ability Name or Number(1-3): ')
    
    if(not act_ans.lower() in ["slash","fireball","hp sacrifice","1","2","3"]):
        cls()
        print(f'\n\n\nNOT A STARTING ABILITY')
        continue
    if act_ans.lower()=="1":
        act_ans="slash"
    elif act_ans.lower()=="2":
        act_ans="fireball"
    elif act_ans.lower()=="3":
        act_ans="hp sacrifice"


    new_ability=Ability(act_ans)
    player.add_ability(new_ability)
    new_ability2=Ability("guard")
    player.add_ability(new_ability2)

    opp_ability=Ability("fireball")
    opp.add_ability(opp_ability)
    opp_ability2=Ability("guard")
    opp.add_ability(opp_ability2)
    
    print(player.abilities)
    print("You picked "+ player.abilities[0].ability["name"])
    print("Opp picked "+ opp.abilities[-1].ability["name"]+" and "+opp.abilities[-2].ability["name"]+"\n\n")

    while(round_number<=10):
        if(round_number>=1):
            opp.max_hp+=10
        if(round_number%2==0 and round_number!=0):
            opp.add_random_ability()
        round_number+=1
        opp.hp=opp.max_hp
        opp.mana=opp.max_mana
        player.mana=player.max_mana
        opp.statuses=[]
        player.statuses=[]
        rand_weather=field_conditions["weather"][randint(0,len(field_conditions["weather"])-1)]
        rand_terrain=field_conditions["terrain"][randint(0,len(field_conditions["terrain"])-1)]
        game_field=GameField(rand_weather,rand_terrain)
        player.block=0
        opp.block=0
        while(player.hp>0 and opp.hp>0):
            
            # print(rand_weather)
            # print(rand_terrain)
            cls()
            print("=====================================\033[1mCombat #"+str(round_number)+"\033[0m=====================================")
            print('\n')
            print(f'Weather: {rand_weather} ------------- Terrain: {rand_terrain} ------------- Accuracies Attacks: x{round(game_field.calculate_accuracy("attack"),2)} Special Moves: x{game_field.calculate_accuracy("special")}\n\n\n')
            player.print_hp_string()
            opp.print_hp_string()

            # print("Your HP: "+str(player.hp)+"/"+str(player.max_hp) +" Block: "+str(player.block) + "\n"+"Opp HP: "+str(opp.hp)+"/"+str(opp.max_hp)+" Block: "+str(opp.block))
            
            
            chosen=False
            while(chosen==False):
                ability_str=""
                count=0
                for e in player.abilities:
                    count+=1
                    ability_str= ability_str+str(count)+". "+e.ability["name"]+" "

                #opponent will do {random move that they will use}
                opp_random=opp.random_ability()
                print(f'\n\033[1m{opp.name} will use {opp_random}\033[0m')
                print("\n\nYour abilities: "+str(ability_str)) 

                print("\n")
                choose_ability=input("Choose an ability to use: ") 
                cls()
                print('\n')
                print((Colors.LIGHT_GRAY+"▓"+Colors.END)*100)
                

                ab_in_player=False
                my_abils_count=0
                for e in player.abilities:
                    my_abils_count+=1
                    if(choose_ability.lower()==e.ability["name"].lower()):
                        ab_in_player=True
                    elif(choose_ability==str(my_abils_count)):
                        choose_ability=e.ability["name"].lower()
                        if e.ability["type"]=="special" and player.class_name=="Wizard":
                            if player.mana-e.ability["mana cost"]<0:
                                print(f'\n\nNOT ENOUGH MANA {player.mana}/{player.max_mana}, MANA COST {e.ability["mana cost"]}\n\n')
                                continue
                        ab_in_player=True
                
                # enter to use default ability
                if(choose_ability==""):
                    ab_in_player=True
                    first_abil=player.abilities[1].ability["name"]
                


                if(ab_in_player):
                    print("\n")
                    if(choose_ability==""):
                        player.activate_ability(first_abil,opp,game_field) 
                    else:
                        player.activate_ability(choose_ability,opp,game_field)  
                    chosen=True
                else: #
                    print("Choose a valid ability...")
                    continue
                
                if(opp.hp<=0):
                    print("YOU WIN!")
                    opp.block=0
                    break
                elif(player.hp<=0):
                    cls()
                    print(f"{Colors.RED}YOU LOSE... GAME OVER{Colors.RED}\n\n")
                    print(player)
                    break
                player.calculated_end_round_status_amount(opp)
                opp.activate_ability(opp_random,player,game_field)
                opp.calculated_end_round_status_amount(player)
                print(f'\n')
                filler=input(f'Press Enter to Continue...\n\n\n{(Colors.LIGHT_GRAY+"▓"+Colors.END)*100}\n\n')
            



        # Upgrade Rewards and new ability
        has_picked=False
        if(player.hp<=0):
            has_picked=True
            cls()
            print(f"{Colors.RED}YOU LOSE... GAME OVER{Colors.END}\n\n")
            break
        
        while(not has_picked):
            shuffle(upgrades)
            cls()
            print(f'\n\n\n{Colors.LIGHT_GREEN}YOU WIN!{Colors.END}\n\n')
            print("CHOOSE YOUR REWARDS")
            print("1. "+upgrades[0]["name"]+" Amount: +"+str(upgrades[0]["amount"])+" ||| 2. "+upgrades[1]["name"]+" Amount: +"+str(upgrades[1]["amount"])+" ||| 3. "+upgrades[2]["name"]+ " Amount: +"+str(upgrades[2]["amount"]))
            print("\n")
            up_ans=input("Pick an upgrade (1, 2, or 3): ")
            
            if(up_ans=="1" or up_ans=="2" or up_ans=='3'):
                player.add_upgrade(upgrades[int(up_ans)-1]["name"],upgrades[int(up_ans)-1]["amount"])
                print(Colors.LIGHT_PURPLE+"\nADDED UPGRADE: "+upgrades[int(up_ans)-1]["name"]+Colors.END)
                # print(player)
                has_picked=True
            else:
                print("Please Enter 1,2, or 3...")
                continue
            
            while True:
                print("\n====================================================================================== \n")
                print("CHOOSE A NEW ABILITY\n")
                player.reward_ability_three()
                new_chosen_ability=input("Choose Ability (1,2, or 3): ")
                if new_chosen_ability=="1" or new_chosen_ability=="2" or new_chosen_ability=="3":
                    print(f'You Picked {player.abilites_to_choose_from[int(new_chosen_ability)-1]}' )
                    player.add_ability(player.abilites_to_choose_from[int(new_chosen_ability)-1])
                    break
                    
                elif new_chosen_ability=="" or new_chosen_ability.lower()=="skip":
                    print("You have chosen to skip.")
                    break


        player.rand_heal()
                
            
        
    isPlaying=False


# print (player.hp)