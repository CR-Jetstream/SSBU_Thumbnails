// 1st image links
let v1 = "first"
let v2 = "first"
let v3 = "first"
let v4 = "first"
$('#v1 .link').addClass(v1);
$('#v2 .link').addClass(v2);
$('#v3 .link').addClass(v3);
$('#v4 .link').addClass(v4);

// Death image links
let d1 = "death"
let d2 = "death"
let d3 = "death"
let d4 = "death"
$('#d1 .link').addClass(d1);
$('#d2 .link').addClass(d2);
$('#d3 .link').addClass(d3);
$('#d4 .link').addClass(d4);

// Update player color based on character (death_)
//Player 1
if (docData['death_1']=='Mario') { document.getElementById("win_1").style.color = "#F2390B"; }
else if (docData['death_1']=='Luigi') { document.getElementById("win_1").style.color = "#4CAB10"; }
else if (docData['death_1']=='Toad') { document.getElementById("win_1").style.color = "#047EFD"; }
else if (docData['death_1']=='Toadette') { document.getElementById("win_1").style.color = "#F950C5"; }
//Player 2
if (docData['death_2']=='Mario') { document.getElementById("win_2").style.color = "#F2390B"; }
else if (docData['death_2']=='Luigi') { document.getElementById("win_2").style.color = "#4CAB10"; }
else if (docData['death_2']=='Toad') { document.getElementById("win_2").style.color = "#047EFD"; }
else if (docData['death_2']=='Toadette') { document.getElementById("win_2").style.color = "#F950C5"; }
//Player 3
if (docData['death_3']=='Mario') { document.getElementById("win_3").style.color = "#F2390B"; }
else if (docData['death_3']=='Luigi') { document.getElementById("win_3").style.color = "#4CAB10"; }
else if (docData['death_3']=='Toad') { document.getElementById("win_3").style.color = "#047EFD"; }
else if (docData['death_3']=='Toadette') { document.getElementById("win_3").style.color = "#F950C5"; }
//Player 4
if (docData['death_4']=='Mario') { document.getElementById("win_4").style.color = "#F2390B"; }
else if (docData['death_4']=='Luigi') { document.getElementById("win_4").style.color = "#4CAB10"; }
else if (docData['death_4']=='Toad') { document.getElementById("win_4").style.color = "#047EFD"; }
else if (docData['death_4']=='Toadette') { document.getElementById("win_4").style.color = "#F950C5"; }

// Update player names from Wins
if ($('#win_1').text() != docData['win_1'] || 
    $('#win_2').text() != docData['win_2'] || 
    $('#win_3').text() != docData['win_3'] ||
    $('#win_4').text() != docData['win_4'] )
{
	// Show players
	$('body')
		.queue(elemUpdate())
		.queue(elemShow('.players'))
	// Show Scores for active players
	if ($('#win_1').text() != "")
		{$('body').queue(elemShow('.wins.w1')).queue(elemShow('.deaths.d1'))
		.queue(elemShow('#v1')).queue(elemShow('#d1'))}
	if ($('#win_2').text() != "")
		{$('body').queue(elemShow('.wins.w2')).queue(elemShow('.deaths.d2'))
		.queue(elemShow('#v2')).queue(elemShow('#d2'))}
	if ($('#win_3').text() != "")
		{$('body').queue(elemShow('.wins.w3')).queue(elemShow('.deaths.d3'))
		.queue(elemShow('#v3')).queue(elemShow('#d3'))}
	if ($('#win_4').text() != "")
		{$('body').queue(elemShow('.wins.w4')).queue(elemShow('.deaths.d4'))
		.queue(elemShow('#v4')).queue(elemShow('#d4'))}
}
// Update player wins from Win score
if ($('#win_1s').text() != docData['win_1s'] ||
	$('#win_2s').text() != docData['win_2s'] ||
	$('#win_3s').text() != docData['win_3s'] ||
    $('#win_4s').text() != docData['win_4s'] ||
	$('#win_1').text() == "" || 
    $('#win_2').text() == "" || 
    $('#win_3').text() == "" ||
    $('#win_4').text() == "" )
{

    $('body').queue(elemUpdate());
        
	if($('#win_1').text() == "")
	{ $('body').queue(elemHide('.wins.w1')) }
	else { $('body').queue(elemShow('.wins.w1')) }
	
	if($('#win_2').text() == "")
	{ $('body').queue(elemHide('.wins.w2')) }
	else { $('body').queue(elemShow('.wins.w2')) }
	
	if($('#win_3').text() == "")
	{ $('body').queue(elemHide('.wins.w3')) }
	else { $('body').queue(elemShow('.wins.w3')) }
	
	if($('#win_4').text() == "")
	{ $('body').queue(elemHide('.wins.w4')) }
	else { $('body').queue(elemShow('.wins.w4')) }
	
}
// Update player deaths from Death score
if ($('#death_1s').text() != docData['death_1s'] ||
	$('#death_2s').text() != docData['death_2s'] ||
	$('#death_3s').text() != docData['death_3s'] ||
    $('#death_4s').text() != docData['death_4s'] ||
    $('#win_1').text() == "" || 
    $('#win_2').text() == "" || 
    $('#win_3').text() == "" ||
    $('#win_4').text() == "" )
{

    $('body').queue(elemUpdate());
        
	if($('#win_1').text() == "")
	{ $('body').queue(elemHide('.deaths.d1')) }
	else { $('body').queue(elemShow('.deaths.d1')) }
	
	if($('#win_2').text() == "")
	{ $('body').queue(elemHide('.deaths.d2')) }
	else { $('body').queue(elemShow('.deaths.d2')) }
	
	if($('#win_3').text() == "")
	{ $('body').queue(elemHide('.deaths.d3')) }
	else { $('body').queue(elemShow('.deaths.d3')) }
	
	if($('#win_4').text() == "")
	{ $('body').queue(elemHide('.deaths.d4')) }
	else { $('body').queue(elemShow('.deaths.d4')) }
	
}

// Update images
if($('#win_1').text() == "")
{ $('body').queue(elemHide('#v1')).queue(elemHide('#d1')) }
else { $('body').queue(elemShow('#v1')).queue(elemShow('#d1')) }

if($('#win_2').text() == "")
{ $('body').queue(elemHide('#v2')).queue(elemHide('#d2')) }
else { $('body').queue(elemShow('#v2')).queue(elemShow('#d2')) }

if($('#win_3').text() == "")
{ $('body').queue(elemHide('#v3')).queue(elemHide('#d3')) }
else { $('body').queue(elemShow('#v3')).queue(elemShow('#d3')) }

if($('#win_4').text() == "")
{ $('body').queue(elemHide('#v4')).queue(elemHide('#d4')) }
else { $('body').queue(elemShow('#v4')).queue(elemShow('#d4')) }