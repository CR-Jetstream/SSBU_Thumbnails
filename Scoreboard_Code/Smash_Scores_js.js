if ($('#player_1').text() != docData['player_1'] ||
    $('#player_2').text() != docData['player_2'] )
{
    $('body')
        .queue(elemHide('.scores')).delay(500)
        .queue(elemHide('.players')).delay(500)
        .queue(elemUpdateSingle('player_1'))	
        .queue(elemUpdateSingle('player_2'))
        .queue(elemUpdateSingle('player_1s'))	
        .queue(elemUpdateSingle('player_2s')).delay(500)
        .queue(elemShow('.players')).delay(500)
        .queue(elemShow('.scores')).delay(500);
}
else if ($('#player_1s').text() != docData['player_1s'] ||
    $('#player_2s').text() != docData['player_2s'] )
{
    $('body')
        .queue(elemHide('.scores')).delay(500)
        .queue(elemUpdateSingle('player_1s'))	
        .queue(elemUpdateSingle('player_2s')).delay(500)
        .queue(elemShow('.scores')).delay(500);
}

if ($('#event_1').text() != docData['event_1'])
{
	    $('body')
        .queue(elemHide('.event')).delay(500)
        .queue(elemUpdateSingle('event_1')).delay(500)
        .queue(elemShow('.event')).delay(500);
}

if ($('#round_1').text() != docData['round_1'])
{
	    $('body')
        .queue(elemHide('.round')).delay(500)
        .queue(elemUpdateSingle('round_1')).delay(500)
        .queue(elemShow('.round')).delay(500);
}