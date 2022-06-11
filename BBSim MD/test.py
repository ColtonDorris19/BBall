from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix import MDAdaptiveWidget
from kivy.uix.screenmanager import ScreenManager
from kivy.properties import StringProperty, BooleanProperty, ObjectProperty, NumericProperty
import random
from kivymd.uix.behaviors import RoundedRectangularElevationBehavior
from kivymd.uix.card import MDCard
from kivy.utils import get_color_from_hex
from kivy.core.window import Window

Window.size = (360,700)


class Player():
    def __init__(self,name,pos,off,deff,reb, att_three,three_dist):
        self.name = name
        self.pos = pos
        self.off = off
        self.deff = deff
        self.stats = 0
        #self.three = three
        self.reb = reb
        self.reb_stats = 0
        self.shots = 0
        self.att_three = att_three
        self.three_attempt = 0
        self.three_made = 0
        self.fg_made = 0
        self.three_dist = three_dist

class Team():
    def __init__(self, name, pg, sg, sf, pf, c):
        self.name = name
        self.pg = pg
        self.sg = sg
        self.sf = sf
        self.pf = pf
        self.c = c
        self.score = 0
        self.results = None
        self.to = 0
        self.players = None

    def set_roster(self):
            self.players = [self.pg, self.sg, self.sf, self.pf, self.c]
        

###############################################################################################################################################################
######################################################################## GAME CODE ############################################################################
###############################################################################################################################################################

class Game():
    def __init__(self,home,away):
        self.home=home
        self.away=away
        self.poss=0
        self.clock=0
        self.hw=0
        self.aw=0
        self.results = "Tipoff \n"
        self.series = 1
        self.home.set_roster()
        self.away.set_roster()
        self.shooter = None
        self.on_ball = None
        self.shot_type = None
        

    
    def shot_selector(self, team, deff):
        pg = .2
        sg = pg + .2
        sf = sg +.2
        pf = sf + .2
        c = pf + .2
        x = random.random()


#I think the function below needs to only set the "shooter" and "defender", and then combine "select_shot()" into this to return
#actors list along with the type of shot. if not, you'd have to write select_shot parameters to include a list that contains a list and a string. 
        if x <= pg:
            self.shooter = team.pg
            self.on_ball = deff.pg
        elif x <= sg:
            self.shooter = team.sg
            self.on_ball = deff.sg
        elif x <= sf:
            self.shooter = team.sf
            self.on_ball = deff.sf
        elif x <= pf:
            self.shooter = team.pf
            self.on_ball = deff.pf
        elif x <= c:
            self.shooter = team.c
            self.on_ball = deff.c

        #Figure out shot type
        three_chance = self.shooter.three_dist
        x = random.random()
        if three_chance > x:
            self.shot_type = 3
            self.three_attempt()
        else: 
            self.shot_type = 2
            self.fg_attempt()


    def three_attempt(self):
        variance = 3.1 - self.on_ball.deff*.0199
        shot_min = 100 - variance
        shot_max = 100 + variance
        shot = random.gauss(100,(9.5-(self.shooter.att_three/13)))
        self.shooter.shots += 1
        self.shooter.three_attempt += 1
        if shot_min < shot < shot_max:
            self.shooter.three_made += 1
            self.shooter.fg_made += 1
            self.shooter.stats += 3
            if self.poss == 0:
                self.home.score += 3
            else: self.away.score += 3
            self.results += (f"{self.clock} - {self.shooter.name} made three pointer! {self.home.score} - {self.away.score} \n")
        else: 
            self.results += (f"{self.clock} - {self.shooter.name} missed three pointer. - ")
            self.rebound()

    def fg_attempt(self):
        if self.shooter.off < 55:
            trash = .50
            if self.shooter.off < 50:
                trash = 1
        else:
            trash = 0
        variance = 3.8 - self.on_ball.deff*.019-trash
        shot_min = 100 - variance
        shot_max = 100 + variance
        shot = random.gauss(100,(9.5+trash-(self.shooter.off/13)))
        self.shooter.shots += 1
        if shot_min < shot < shot_max:
            self.shooter.stats += 2
            self.shooter.fg_made += 1
            if self.poss == 0:
                self.home.score += 2
            else: self.away.score += 2
            self.results += (f"{self.clock} - {self.shooter.name} made field goad! {self.home.score} - {self.away.score} \n")
            
        else: 
            self.results += (f"{self.clock} - {self.shooter.name} missed field goal. - ")
            self.rebound()
        
    def rebound(self):
        location = random.random()
        chance = random.random()
        if self.poss == 0: 
            off = self.home
            deff = self.away
        else:
            off = self.away
            deff = self.home
        if location <= .12: #PG
            if (chance + (deff.pg.reb -off.pg.reb)*.004) > .24:
                self.results += (f"{deff.pg.name} defensive rebound \n")
                deff.pg.reb_stats += 1
                return
            else:
                self.results += (f"{off.pg.name} offensive rebound \n")
                off.pg.reb_stats += 1
                self.switch_poss()
                return
        if .12 < location <= .26: #SG
            if (chance + (deff.sg.reb -off.sg.reb)*.004) > .24:
                self.results += (f"{deff.sg.name} defensive rebound \n")
                deff.sg.reb_stats += 1
                return
            else:
                self.results += (f"{off.sg.name} offensive rebound \n")
                off.sg.reb_stats += 1
                self.switch_poss()
                return
        if .26 < location <= .48: #SF
            if (chance + (deff.sf.reb -off.sf.reb)*.004) > .24:
                self.results += (f"{deff.sf.name} defensive rebound \n")
                deff.sf.reb_stats += 1
                return
            else:
                self.results += (f"{off.sf.name} offensive rebound \n")
                off.sf.reb_stats += 1
                self.switch_poss()
                return
        if .48 < location <= .72: #PF
            if (chance + (deff.pf.reb -off.pf.reb)*.004) > .24:
                self.results += (f"{deff.pf.name} defensive rebound \n")
                deff.pf.reb_stats += 1
                return
            else:
                self.results += (f"{off.pf.name} offensive rebound \n")
                off.pf.reb_stats += 1
                self.switch_poss()
                return
        if location > .72: #C
            if (chance + (deff.c.reb -off.c.reb)*.004) > .24:
                self.results += (f" {str(self.clock)} - {deff.c.name} defensive rebound \n")
                deff.c.reb_stats += 1
                return
            else:
                self.results += (f"{off.c.name} offensive rebound \n")
                off.c.reb_stats += 1
                self.switch_poss()
                return
        



    def check_clock(self):
        if self.clock > 2400:
            return False

    def scorekeeping(self):
        pass


    def switch_poss(self):
        if self.poss == 0:
            self.poss = 1
        else: self.poss = 0
            
    def tip_off(self):
        if random.randrange(0,2) == 0:
            self.poss = 0
        else: self.poss =1
            
    def run_time_poss(self):
        self.clock=self.clock+random.gauss(14,5)
            
    def home_poss(self):
        self.run_time_poss()
        if self.check_clock() == False: return
        turnover_value = (self.home.pg.off + self.home.sg.off + self.home.sf.off+self.home.sf.off+self.home.c.off-(self.away.pg.deff+self.away.sg.deff+self.away.sf.deff+self.away.pf.deff+self.away.c.deff))*.0016
        to_chance = random.random() - turnover_value
        ########### START HERE ################
        if to_chance < 0.12:
            self.results += (f"{self.clock} - HOME TEAM TURNED THE BALL OVER!! \n")
            self.home.to += 1
            self.switch_poss()
        else:
            self.shot_selector(self.home,self.away)
            self.switch_poss()
            

        

                      
        
    def away_poss(self):
        self.run_time_poss()
        if self.check_clock() == False: return
        turnover_value = (self.away.pg.off + self.away.sg.off + self.away.sf.off+self.away.sf.off+self.away.c.off-(self.home.pg.deff+self.home.sg.deff+self.home.sf.deff+self.home.pf.deff+self.home.c.deff))*.0016
        to_chance = random.random() - turnover_value
        if to_chance < 0.15:
            self.results += (f"{self.clock} - AWAY TEAM TURNED THE BALL OVER!! \n")
            self.away.to += 1
            self.switch_poss()
            
        else:
            self.shot_selector(self.away,self.home)
            self.switch_poss()
                      
                      
        
    def play(self):
        while self.hw + self.aw < self.series:
            self.home.score = 0
            self.away.score = 0
            while self.clock < 2400:
                if self.poss == 0:
                    self.home_poss()
                else: self.away_poss()
            self.clock = 0
            if self.home.score > self.away.score:
                self.hw=self.hw+1
            elif self.home.score == self.away.score:
                self.results += (f"0.00 - TIED UP AT THE END OF REGULATION \n \n300 - BEGIN OVERTIME")
                self.clock=300
                continue
            else:
                self.aw=self.aw+1
                
            






#####################################################################################################################
#####################################################################################################################
#####################################################################################################################
#####################################################################################################################



pg1 = Player("Dee Dee Smith", "PG", 75, 80,75, 77, .3)
sg1 = Player("Roger Huntley","SG", 61,80,75, 90, .45)
sf1 = Player("Malcolm Smith", "SF",79 ,80,77, 72, .2)
pf1 = Player("George Fant", "PF",79 ,80, 75, 65, .1)
c1 = Player("Alex Poythresse", "C", 88,80, 80, 65, .05)

team1 = Team("Hilltoppers", pg1,sg1,sf1,pf1,c1)

pg2 = Player("Dimes McGee", "PG", 75, 80, 75, 77, .3)
sg2 = Player("Shooter McGavock", "SG", 75,80, 75, 90, .45)
sf2 = Player("Samuel Driver", "SF", 75 ,80, 75, 72, .2)
pf2 = Player("Big Earl", "PF",75 ,80, 75, 65, .1)
c2 = Player("Simon Tower", "C",75,80, 75, 65, .05)

team2= Team("Governors", pg2,sg2,sf2,pf2,c2)
game = Game(team1, team2)
teams = [team1, team2]
class WindowManager(ScreenManager):
    pass





###########  Screens #############################
################### SCREENS ######################
########################## SCREENS!!! ############

class StartPage(Screen, MDAdaptiveWidget):
    user = team1
    ai = team2

class TeamPage(Screen, MDAdaptiveWidget):

    def test():
        print("Hi")

    def edit_player(self, player):
        self.manager.get_screen("edit_player").player = player

    def calc_overall(self):
        overall = 0
        for i in team1.players:
            overall += (i.off +i.deff +i.att_three +i.reb)
        overall = overall / 20
        return str(overall)
    def calc_overall2():
        yeet = 0
        for i in team2.players:
            yeet += (i.off +i.deff +i.att_three +i.reb)
        yeet = yeet /20
        return str(yeet)
    
    def calc_total_att(self):
        att_count = 750 - (pg1.off+pg1.deff+sg1.off+sg1.deff+sf1.off+sf1.deff+pf1.off+pf1.deff+c1.off+c1.deff)
        return att_count
    team = team1
    ovr2 = calc_overall2()
    att_count = 750
    pg1_name = StringProperty(" ")
    att_pts = StringProperty(str(att_count))
    pgoff = StringProperty("Offense: 75")
    pgdeff = StringProperty("Defense: 80")
    sgoff = StringProperty("Offense: 61")
    sgdeff = StringProperty("Defense: 80")
    sfoff = StringProperty("Offense: 79")
    sfdeff = StringProperty("Defense: 80")
    pfoff = StringProperty("Offense: 79")
    pfdeff = StringProperty("Defense: 80")
    coff = StringProperty("Offense: 88")
    cdeff = StringProperty("Defense: 80")
    overall = StringProperty("77")
    overall2 = StringProperty(ovr2)
    team = team1

###      PG - Point Guard     ###################################################################
    def pg1_name_val(self, widget):
        pg1.name = widget.text
            


    def pg1_off_val(self, widget):
        pg1.off = int(widget.value)
        self.att_count = self.calc_total_att()
        self.att_pts = str(self.att_count)
        self.pgoff = "Offense: " + str(int(widget.value))
        self.overall = self.calc_overall()
    def pg1_deff_val(self, widget):
        pg1.deff = int(widget.value)
        self.att_count = self.calc_total_att()
        self.att_pts = str(self.att_count)
        self.pgdeff = "Defense: " + str(int(widget.value))

        
###      SG - Shooting Guard     ###################################################################

    
    def sg1_name_val(self, widget):
        sg1.name = widget.text

    def sg1_off_val(self, widget):
        sg1.off = int(widget.value)
        self.att_count = self.calc_total_att()
        self.att_pts = str(self.att_count)
        self.sgoff = "Offense: " + str(int(widget.value))

    def sg1_deff_val(self, widget):
        sg1.deff = int(widget.value)
        self.att_count = self.calc_total_att()
        self.att_pts = str(self.att_count)
        self.sgdeff = "Defense: " + str(int(widget.value))
        
###      SF - Small Forward     ###################################################################
    def sf1_name_val(self, widget):
        sf1.name = widget.text

    def sf1_off_val(self, widget):
        sf1.off = int(widget.value)
        self.att_count = self.calc_total_att()
        self.att_pts = str(self.att_count)
        self.sfoff = "Offense: " + str(int(widget.value))

    def sf1_deff_val(self, widget):
        sf1.deff = int(widget.value)
        self.att_count = self.calc_total_att()
        self.att_pts = str(self.att_count)
        self.sfdeff = "Defense: " + str(int(widget.value))

###      PF - Power Forward     ###################################################################
    def pf1_name_val(self, widget):
        pf1.name = widget.text

    def pf1_off_val(self, widget):
        pf1.off = int(widget.value)
        self.att_count = self.calc_total_att()
        self.att_pts = str(self.att_count)
        self.pfoff = "Offense: " + str(int(widget.value))

    def pf1_deff_val(self, widget):
        pf1.deff = int(widget.value)
        self.att_count = self.calc_total_att()
        self.att_pts = str(self.att_count)
        self.pfdeff = "Defense: " + str(int(widget.value))

###      C - Center    ###################################################################
    def c1_name_val(self, widget):
        c1.name = widget.text

    def c1_off_val(self, widget):
        c1.off = int(widget.value)
        self.att_count = self.calc_total_att()
        self.att_pts = str(self.att_count)
        self.coff = "Offense: " + str(int(widget.value))

    def c1_deff_val(self, widget):
        c1.deff = int(widget.value)
        self.att_count = self.calc_total_att()
        self.att_pts = str(self.att_count)
        self.cdeff = "Defense: " + str(int(widget.value))

    def sim(self):
        game.tip_off()
        game.play()
        self.manager.get_screen("results").final_score = (str(team1.score) + " - " + str(team2.score))
        self.manager.get_screen("results").record = (str(game.hw) + " - " + str(game.aw))
        self.manager.get_screen("post_stats").update(0)
######################################################################################################################
############################################### Results ##############################################################
######################################################################################################################


class EditPage(Screen, MDAdaptiveWidget):
    player_to_edit = pg1
    player_name = StringProperty(" ")
    player_position = StringProperty(" ")
    name_input = "Name Here"
    off_slider = 0
    deff_slider = 0
    rebounding_slider = 0
    three_slider = 0
    three_dist_slider = 0
    
    def on_name_input(self,widget):
        self.name_input = widget.text
    
    def on_off_slider(self, widget):
        self.off_slider = int(widget.value)
        

    def on_deff_slider(self, widget):
        self.deff_slider = int(widget.value)
        

    def on_rebounding_slider(self, widget):
        self.rebounding_slider = int(widget.value)

    def on_three_slider(self, widget):
        self.three_slider = int(widget.value)

    def on_three_dist_slider(self, widget):
        self.three_dist_slider = int(widget.value)
        
        
        

    def update(self, player):
        self.player_to_edit = player
        self.player_name = player.name
        self.player_position = player.pos

    def save(self):
        if self.name_input != "Name Here":
            self.player_to_edit.name = self.name_input
        self.player_to_edit.off = self.off_slider
        self.player_to_edit.deff = self.deff_slider
        self.player_to_edit.reb = self.rebounding_slider
        self.player_to_edit.att_three = self.three_slider
        self.player_to_edit.three_dist = self.three_dist_slider       


class ResultsPage(Screen, MDAdaptiveWidget):
    final_score = StringProperty(str(team1.score))
    record = StringProperty(" ")


        
        

class SettingsPage(Screen, MDAdaptiveWidget):
    def series(self, x):
        game.series = x



class PostStatsPage(Screen, MDAdaptiveWidget):
    n = 0
    opp_name = StringProperty(" ")
    score = StringProperty(" ")
    name1 = StringProperty(" ")
    name2 = StringProperty(" ")
    name3 = StringProperty(" ")
    name4 = StringProperty(" ")
    name5 = StringProperty(" ")
    stats1 = StringProperty(" ")
    stats2 = StringProperty(" ")
    stats3 = StringProperty(" ")
    stats4 = StringProperty(" ")
    stats5 = StringProperty(" ")
    fg1 = StringProperty(" ")
    fg2 = StringProperty(" ")
    fg3 = StringProperty(" ")
    fg4 = StringProperty(" ")
    fg5 = StringProperty(" ")
    rebs1 = StringProperty(" ")
    rebs2 = StringProperty(" ")
    rebs3 = StringProperty(" ")
    rebs4 = StringProperty(" ")
    rebs5 = StringProperty(" ")
    threes1 = StringProperty(" ")
    threes2 = StringProperty(" ")
    threes3 = StringProperty(" ")
    threes4 = StringProperty(" ")
    threes5 = StringProperty(" ")
    
    def get_n(self):
        if self.n == 0:
            self.n = 1
            return 1
        else:
            self.n = 0
            return 0

    def update(self,n=0):
        team = teams[n]
        if n == 0:
            self.opp_name = teams[1].name
        else:
            self.opp_name = teams[0].name
        self.team_name = team.name
        self.score = (str(team1.score) + " - " + str(team2.score))
        self.name1 = team.pg.name
        self.name2 = team.sg.name
        self.name3 = team.sf.name
        self.name4 = team.pf.name
        self.name5 = team.c.name
        self.stats1 = str(team.pg.stats)
        self.stats2 = str(team.sg.stats)
        self.stats3 = str(team.sf.stats)
        self.stats4 = str(team.pf.stats)
        self.stats5 = str(team.c.stats)
        self.fg1 = str(int(team.pg.fg_made)) + "/" + str(team.pg.shots)
        self.fg2 = str(int(team.sg.fg_made)) + "/" + str(team.sg.shots)
        self.fg3 = str(int(team.sf.fg_made)) + "/" + str(team.sf.shots)
        self.fg4 = str(int(team.pf.fg_made)) + "/" + str(team.pf.shots)
        self.fg5 = str(int(team.c.fg_made)) + "/" + str(team.c.shots)
        self.rebs1 = str(team.pg.reb_stats)
        self.rebs2 = str(team.sg.reb_stats)
        self.rebs3 = str(team.sf.reb_stats)
        self.rebs4 = str(team.pf.reb_stats)
        self.rebs5 = str(team.c.reb_stats)
        self.threes1 = str(team.pg.three_made) + "/" +str(team.pg.three_attempt)
        self.threes2 = str(team.sg.three_made) + "/" +str(team.sg.three_attempt)
        self.threes3 = str(team.sf.three_made) + "/" +str(team.sf.three_attempt)
        self.threes4 = str(team.pf.three_made) + "/" +str(team.pf.three_attempt)
        self.threes5 = str(team.c.three_made) + "/" +str(team.c.three_attempt)
        


class InfoPage(Screen, MDAdaptiveWidget):
    text1 = """Thank you for taking the time to test this application. There's a TON of formulas and algorithms to iron out in order to accurately simulate a basketball game. I could spend \
all my time testing and analyzing different combination outcomes just in the game's current state, so any and all feedback from you is valuable. 

I've included a \"Roadmap\" of planned features with their optimistic release dates. I've also tried to cover my vision for the game's final release state. As this game \
continues to develop, let me know if you think of any additional features you think would make the game more fun.

Use www.trello.com/D1Hoops to provide feedback and report bugs. 

.................."""


class MD3Card(MDCard, RoundedRectangularElevationBehavior):
    pass


class TestApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.accent_palette = "Orange"
        #self.theme_cls.theme_style="Dark"
        #return Builder.load_file('test.kv')

    main_team = ObjectProperty(None)
    secondary_team = ObjectProperty(None)
    main_team_name = main_team.name
    secondary_team_name = secondary_team.name
    name1 = StringProperty(team1.pg.name)
    name2 = StringProperty(team1.sg.name)
    name3 = StringProperty(team1.sf.name)
    name4 = StringProperty(team1.pf.name)
    name5 = StringProperty(team1.c.name)

    off1 = NumericProperty(0)
    off2 = NumericProperty(0)
    off3 = NumericProperty(0)
    off4 = NumericProperty(0)
    off5 = NumericProperty(0)

    deff1 = NumericProperty(0)
    deff2 = NumericProperty(0)
    deff3 = NumericProperty(0)
    deff4 = NumericProperty(0)
    deff5 = NumericProperty(0)

    reb1 = NumericProperty(0)
    reb2 = NumericProperty(0)
    reb3 = NumericProperty(0)
    reb4 = NumericProperty(0)
    reb5 = NumericProperty(0)

    att_three1 = NumericProperty(0)
    att_three2 = NumericProperty(0)
    att_three3 = NumericProperty(0)
    att_three4 = NumericProperty(0)
    att_three5 = NumericProperty(0)

    
    

    def update(self,main_team, secondary_team):
        self.main_team = main_team
        self.secondary_team = secondary_team
        self.name1 = main_team.pg.name
        self.name2 = main_team.sg.name
        self.name3 = main_team.sf.name
        self.name4 = main_team.pf.name
        self.name5 = main_team.c.name
        
        self.off1 = main_team.pg.off
        self.off2 = main_team.sg.off
        self.off3 = main_team.sf.off
        self.off4 = main_team.pf.off
        self.off5 = main_team.c.off

        self.deff1 = main_team.pg.deff
        self.deff2 = main_team.sg.deff
        self.deff3 = main_team.sf.deff
        self.deff4 = main_team.pf.deff
        self.deff5 = main_team.c.deff

        self.reb1 = main_team.pg.reb
        self.reb2 = main_team.sg.reb
        self.reb3 = main_team.sf.reb
        self.reb4 = main_team.pf.reb
        self.reb5 = main_team.c.reb

        self.att_three1 = main_team.pg.att_three
        self.att_three2 = main_team.sg.att_three
        self.att_three3 = main_team.sf.att_three
        self.att_three4 = main_team.pf.att_three
        self.att_three5 = main_team.c.att_three
        




TestApp().run()