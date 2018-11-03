# vsa_game_server
Server which enables chat and cooperative game play

## Features
1. Single line text-based protocol (utf-8)
2. Send messages to users or groups that have registered for a service
3. Receive messages from users or groups that have registered for a service
3. Extensible to new services without having to touch the server

## Security
1. Log all messages on the server
2. Require a password to connect
3. TODO: user accounts managed through website

## Protocol

<pre>
SEND format: TOUSER:PROGRAM:PAYLOAD
RECV format: FROMUSER:TOUSER:PROGRAM:PAYLOAD

FROMUSER = <USER>
TOUSER = GROUP | ALL | <USER>
</pre>

## SYS user

Users send a message to SYS to register a REQUEST in order to receive messages.

<pre>
SYS:REG:FROMUSER:TOUSER:PROGRAM - enable this message flow
SYS:UNREG:REQUFROMUSER:TOUSER:PROGRAMEST - disable this message flow
SYS:REGLIST - send back a list of what you've registered for
SYS:USERLIST - send back a list of all users
</pre>

## Examples

### Private chat

<pre>
SEND: SYS:REG:DAVID:EDDIE:CHAT
SEND: EDDIE:CHAT:Hey, what's up?
RECV: EDDIE:DAVID:CHAT:Not much. How about you?
SEND: EDDIE:CHAT:See you later.
SEND: SYS:UNREG:DAVID:EDDIE:CHAT
</pre>

### Group chat

<pre>
SEND: SYS:REG:DAVID:ALL:CHAT
SEND: ALL:CHAT:Hey, is anybody there?
RECV: SARAH:ALL:CHAT:We're all here!
RECV: JOHN:ALL:CHAT:Yes
RECV: LISA:ALL:CHAT:Yep
SEND: ALL:CHAT:Great
</pre>

### Tic Tac Toe game

<pre>
SEND: SYS:REG:DAVID:EDDIE:TICTAC
SEND: EDDIE:TICTAC:3
RECV: EDDIE:DAVID:TICTAC:7
SEND: EDDIE:TICTAC:2
RECV: EDDIE:DAVID:TICTAC:6
SEND: EDDIE:TICTAC:1
RECV: EDDIE:DAVID:TICTAC:8
SEND: EDDIE:TICTAC:0
RECV: EDDIE:DAVID:TICTAC:4
</pre>
