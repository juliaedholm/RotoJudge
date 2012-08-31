# Create your views here.
# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.loader import get_template
from django.template import Context, RequestContext
import models
from models import FootballViewWeeklyMatchResults
from models import FootballViewWeeklyStats
from models import FootballTeams
from models import FootballViewStartOptimal
from models import FootballViewOptimalPercentages
from models import FootballViewStartResults
from models import FootballViewOptimalPercentagesSeason
from models import FootballViewPickValuesTeam
import datetime

def home(request):
   return render_to_response('heroHome.html')

def CreateAccount(request):
    t = get_template('CreateAccount.html')
    c = RequestContext(request, {'smiley':'cheese',})
    return HttpResponse(t.render(c))

def loginPage(request):
    t = get_template('registration:login.html')
    c = RequestContext(request, {'blah':'cheese',})
    return HttpResponse(t.render(c))
    #return render_to_response('TestC.html',{'blah':'buh',}, context_instance=RequestContext(request))

def LeagueSample(request):
    ownersInLeague=FootballTeams.objects.filter(rj_league_id='1')
    t = get_template('SampleLeagueA.html')
    gameList = FootballMainWeeklyMatchResults.objects.filter(week_num='1')  
    c = Context({'pageType':'LeagueSample', 'valueList': '','ownerList': ownersInLeague , 'matchList': gameList})
    return HttpResponse(t.render(c))
 
def OptimalStarts(request):
    return render_to_response('DreamTeam.html', { 'pageType':'stats'} )

def StartingPercentages(request):
    return render_to_response('StartingPercentages.html' )

def PlayerValues(request):
    ownersInLeague=FootballTeams.objects.filter(rj_league_id='1')
    return render_to_response('PlayerValues.html',  )
 
def LeagueHomePage(request, league_id):
    ownersInLeague=FootballTeams.objects.filter(rj_league_id=league_id)
    t = get_template('LeagueHome.html')
    gameList = FootballViewWeeklyMatchResults.objects.filter(week_num='1')
    pickValueSeason=FootballViewPickValuesTeam.objects.filter(rj_league_id=league_id).order_by("-total_team_pick_value")
    seasonPercentagesLeague=FootballViewOptimalPercentagesSeason.objects.filter(rj_league_id=league_id)
    c = Context({'pageType':'LeagueHome', 'valueList': '','ownerList': ownersInLeague , 'matchList': gameList,
                 'pickValuesLeague': pickValueSeason,
                 'leagueID': league_id, 'seasonPercentagesLeague':seasonPercentagesLeague})
    return HttpResponse(t.render(c))

def TeamOwnerPage (request, owner_id, league_id):
    ownersInLeague=FootballTeams.objects.filter(rj_league_id=league_id)
    startPercentageSeason=FootballViewOptimalPercentagesSeason.objects.filter(rj_team_id=owner_id)
    pickValueSeason=FootballViewPickValuesTeam.objects.filter(rj_team_id=owner_id)
    teamOwner=FootballTeams.objects.get(rj_team_id=owner_id)
    smartStartList=FootballViewOptimalPercentages.objects.filter(rj_team_id=owner_id).order_by("week_num")
    erListNum=FootballViewWeeklyStats.objects.filter( rj_team_id=owner_id).order_by("-pick_value")
    erListPosition=FootballViewWeeklyStats.objects.filter( rj_team_id=owner_id).order_by("player_position")
    startResults=FootballViewStartResults.objects.filter(rj_team_id=owner_id).order_by("player_position")
    ownerOptimalStart=FootballViewStartOptimal.objects.filter(rj_team_id=owner_id).order_by("player_position")
    return render_to_response('TeamOwnerPage.html', { 'ownerInfo': teamOwner, 'leagueID': league_id,
                                                     'optimalStartList':ownerOptimalStart, 'valueByNum': erListNum,
                                                     'valueByPos': erListPosition,
                                                     'ownerList': ownersInLeague, 'goodStartList':smartStartList,
                                                     'startResults':startResults, 'startPercentSeason': startPercentageSeason,
                                                     'pickValueSeason': pickValueSeason} )
        
def LeagueRankings(request):
    ownersInLeague=FootballTeams.objects.filter(rj_league_id='1')
    return render_to_response('LeagueRankings.html', { 'pageType':'LeagueRankings', 'ownerList': ownersInLeague} )



