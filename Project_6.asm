TITLE Project_6    (Project_6.asm)

; Author:	Gage McPursifull
; Last Modified:	
; OSU email address: pursifur@oregonstate.edu
; Course number/section:	CS 271
; Project Number: Project 6	                Due Date: 6/7/2020
; Description: This program makes use of macros "GetString" and "DisplayString". Which get and display strings, respectively. 
; The procedure "intro" displays the title, header, and instructions. The procedure ReadVal takes 10 integers in the range 
; [-(2^31) ... (2^31 - 1)] as strings, converts them to integers, then stores them in memory. "sum" sums those integers. "average" 
; calculates the average of those integers. "WriteVal" takes integers as an input, converts them to strings, then displays them.

INCLUDE Irvine32.inc

; Macros 

; GetString Macro ------------------------------------------------------------------------------------------------------------------------------
GetString		MACRO string, prompt, count
	push	eax
	push	ecx
	push	edx
	mov		edx, prompt
	call	WriteString
	mov		edx, string
	mov		ecx, 50
	call	ReadString
	mov		string, edx
	mov		count, eax
	pop		edx
	pop		ecx
	pop		eax
ENDM
; -------------------------------------------------------------------------------------------------------------------------------------------- 

; DisplayString Macro --------------------------------------------------------------------------------------------------------------------------
DisplayString	MACRO string
	push	edx
	mov		edx, string
	call	WriteString
	pop		edx
ENDM
; -----------------------------------------------------------------------------------------------------------------------------------------------

.data

; Messages --------------------------------------------------------------------------------------------------------------------------------------
title_1			BYTE		"            Program 5       ",0
my_name			BYTE		"            Gage McPursifull        ",0
instructions	BYTE		"Enter 10 integers that fit inside a 32 bit register. I'll display a list of the integers, their sum, and average.",0
enter_mess		BYTE		"Enter an integer: ",0
error_mess		BYTE		"Error: either the number was too big, or it was not an integer.",0		
sum_mess		BYTE		"The sum of the integers is: ",0
average_mess	BYTE		"The rounded average of the integers is: ",0
list_mess		BYTE		"Integers entered: ",0
goodbye_mess	BYTE		"See you later",0
;------------------------------------------------------------------------------------------------------------------------------------------------

; User Input-------------------------------------------------------------------------------------------------------------------------------------
user_int		BYTE		50 DUP(0)		; A placeholder for the integer that a user will enter
; -----------------------------------------------------------------------------------------------------------------------------------------------

; Output ----------------------------------------------------------------------------------------------------------------------------------------
int_list		SDWORD		11 DUP(?)		; The list of user entered integers
list_sum		SDWORD		?				; The sum of the integers entered by the user
list_avg		SDWORD		?				; The average of the integers entered by the user
space			BYTE		"   ",0			; A space to be displayed between integers
; -----------------------------------------------------------------------------------------------------------------------------------------------

; Variables ---------------------------------------------------------------------------------------------------------------------------------
byte_count		DWORD		?				; Keeps track of string length after ReadString is called
negative		DWORD		0
; -------------------------------------------------------------------------------------------------------------------------------------------
.code
main PROC

; Call  intro -----------------------------------------------------------------------------------------------------------------------------------
	push	OFFSET instructions
	push	OFFSET my_name
	push	OFFSET title_1
	call	intro
	call	CrLf
; -----------------------------------------------------------------------------------------------------------------------------------------------

; Call ReadVal ----------------------------------------------------------------------------------------------------------------------------------
	push	OFFSET negative
	push	byte_count
	push	OFFSET error_mess
	push	OFFSET enter_mess
	push	OFFSET user_int
	push	OFFSET int_list
	call	ReadVal
	call	CrLf
; -----------------------------------------------------------------------------------------------------------------------------------------------

; Call Sum Process -----------------------------------------------------------------------------------------------------------------------------------------
	push	OFFSET int_list
	push	OFFSET list_sum
	call	sum	
; -----------------------------------------------------------------------------------------------------------------------------------------------

; Call Average Process --------------------------------------------------------------------------------------------------------------------------
	push	list_sum
	push	OFFSET list_avg
	call	average
; -----------------------------------------------------------------------------------------------------------------------------------------------

; Call	WriteVal (list_sum) ------------------------------------------------------------------------------------------------------------------
	push	OFFSET sum_mess
	push	list_sum
	push	OFFSET user_int
	call	WriteVal
	call	CrLf
	call	CrLf

; -----------------------------------------------------------------------------------------------------------------------------------------------

; Call	WriteVal (list_avg) ---------------------------------------------------------------------------------------------------------------------
	push	OFFSET average_mess
	push	list_avg
	push	OFFSET user_int
	call	WriteVal
	call	CrLf
	call	CrLf
; --------------------------------------------------------------------------------------------------------------------------------------------

; Call WriteVal (int_list) ----------------------------------------------------------------------------------------------------------------------

; calls WriteVal once for each element of int_list. On first iteration list_mess is displayed before integer. 
; Subsequent iterations display space before integer.
	mov		ebx, 0
	push	OFFSET list_mess
call_WriteVal_loop:
	add		ebx, 4
	push	[int_list+ebx]
	push	OFFSET user_int
	call	WriteVal
	push	OFFSET space
	cmp		ebx, [SIZEOF int_list - 4]
	jl		call_WriteVal_loop
	call	CrLf
	call	CrLf
	
; -----------------------------------------------------------------------------------------------------------------------------------------------

; Call Goodbye ----------------------------------------------------------------------------------------------------------------------------------
	push	OFFSET goodbye_mess
	call	goodbye
; -----------------------------------------------------------------------------------------------------------------------------------------------

	exit	; exit to operating system
main ENDP

; Introduction Process ---------------------------------------------------------------------------------------------------------------------------
	; Purpose: Display the strings that are passed to the procedure.
	; Receives: title_1 @, my_name @, instructions @.
	; Returns: The strings associated with the input parameters
	; Preconditions: Parameters must be pushed onto stack in the order stated by Stack Frame State.
	; Registers Changed: ebx, ebp

intro	PROC
	push	ebp
	mov		ebp, esp
	push	ebx

	; __________Stack_Frame_State___________
	; ebx				|	[ebp-4]
	; old ebp			|	[ebp]			
	; return @			|	[ebp+4]		
	; title_1 @			|	[ebp+8]
	; my_name @			|	[ebp+12]
	; instructions @	|	[ebp+16]
	; ______________________________________

	mov		ebx, 8					; Set up ebx
	DisplayString	[ebp+ebx]		; display title_1
	add		ebx, 4			
	DisplayString	[ebp+ebx]		; my_name
	call	CrLf
	call	CrLf
	add		ebx, 4
	DisplayString	[ebp+ebx]		; instructions
	call	CrLf

	pop		ebx
	pop		ebp
	ret		12
intro	ENDP
; -----------------------------------------------------------------------------------------------------------------------------------------------

; ReadVal Process ---------------------------------------------------------------------------------------------------------------------------------
	; Purpose: Reads the value of 10 user entered strings, converts the strings to numbers,
	; and validates that they are integers. The results are stored in the array int_list.
	; Receives: int_list @, user_int @, enter_mess @, error_mess @, byte_count
	; Returns: enter_mess prompt
	; Preconditions: Parameters must be pushed onto stack in the order stated by Stack Frame State.
	; Registers Changed: eax, ebx, ecx, edx, edi, esi, ebp

ReadVal		PROC
; Set up Stack Frame and Save used registers
	push	ebp
	mov		ebp, esp
	push	eax
	push	ebx
	push	ecx
	push	edx
	push	edi
	push	esi

	; __________Stack_Frame_State___________
	; saved registers	|	[ebp-]
	; old ebp			|	[ebp]			
	; return @			|	[ebp+4]		
	; int_list @		|	[ebp+8]
	; user_int	@		|	[ebp+12]
	; enter_mess @		|	[ebp+16]
	; error_mess @		|	[ebp+20]
	; byte_count		|	[ebp+24]
	; negative @		|   [ebp+28]
	; ______________________________________


; Set up registers
	mov		esi, [ebp+12]			; esi contains user_int @ (a BYTE array of length 50) used to temp store user input
	mov		edi, [ebp+8]			; edi contains int_list @ (a DWORD array of length 11) used to store numeric values of valid intergers.
	mov		ecx, 10
	add		edi, 4					; Start on the second element of int_list, because for some reason the first element is always 0.

	; Start of outer loop
read_val_loop:
	GetString	esi, [ebp+16], [ebp+24]		; GetString with user_int @, enter_mess @, and byte_count
	push	ecx								; save ecx for out loop 
	mov		ecx, [ebp+24]					; Set ecx equal to byte_count of string just entered.
	
	; Start of inner loop
	; check_pos checks for "+" just for the first character of the entered string.
	; If there is +, decrement ecx and go to compare_low. Otherwise, go to check_neg.
check_pos:
	mov		eax, 0			; Clear eax before lodsb so that eax is equal to al after lodsb
	mov		ebx, 0
	mov		[ebp+28], eax
	lodsb
	mov		bl, 43			; ASCII code for "+"
	cmp		al, bl
	jne		check_neg
	loop	compare_low

	; check_neg checks for "-" just for the first character of the user entered string.
check_neg:
	mov		bl, 45
	cmp		al, bl
	jne		skip_load
	mov		[ebp+28], ecx
	loop	compare_low


	; Take the next digit from a string of digits entered by the user. If the ASCII code is greater than 47, it may be an integer,
	; so jump to compare_high. Otherwise, prompt the user to enter another string.
compare_low:
	mov		eax, 0			; Clear eax before lodsb so that eax is equal to al after lodsb
	mov		ebx, 0
	lodsb
skip_load:
	mov		bl, 47
	cmp		al, bl
	jg		compare_high
	jmp		error

	; Take the digit whose ASCII code is higher than 47, if its ASCII code is lower than 58, it is an integer, so jump to convert.
	; Otherwise, prompt the user to enter another string.
compare_high:
	mov		bl, 58
	cmp		al, bl
	jl		convert_num				
	jmp		error

convert_num:
	sub		al, 48			; The number in al is now equal to the string digit
	push	eax				; Save eax, which is equal to al
	mov		eax, [edi]		; The previous value of [edi] will be a numeric repsentation of the string up to that point.
	mov		ebx, 10
	mov		edx, 0
	imul	ebx				; Multiply eax by 10 to move the place value to the left one spot
	pop		ebx
	jo		error			; If number is greater than 2147483647 (2^31 - 1), or less than -2147483648 jump to error
	push	edx
	mov		edx, 0
	cmp		[ebp+28], edx
	jne		subtract
	pop		edx
	add		eax, ebx		; Then add the current digit to the overall number
	jmp		continue
subtract:
	pop		edx
	sub		eax, ebx
continue:
	jo		error			; If number is greater than 2147483647 (2^31 - 1), or less than -2147483648 jump to error
	mov		[edi], eax
	loop	compare_low	
	add		edi, 4			; At this point [edi] will contain a number equal to the number that is represented by the user entered string.
	

; Prep for reset_esi
	mov		eax, 0
	mov		ebx, 0
	mov		[ebp+28], eax
	mov		ecx, 50

	; This loop resets the values in esi to prevent overflow
	; If not reset, entering too large of numbers - even though invalid - will cause esi to fill up
reset_esi:
	mov		esi, [ebp+12]
	mov		[esi+ebx], eax		; This element of esi is now zero
	inc		ebx
	loop	reset_esi
	call	CrLf
	pop		ecx					; Restore outer loop counter
	dec		ecx					; Here dec ecx/jnz replaces the loop command because the jump distance is more than 128 bytes
	jnz		read_val_loop		; Repeat outer loop if counter is not zero (if we don't have 10 valid numbers yet)
	jmp		read_val_end		; After we have 10 numbers, skip error to end procedure


error:
	DisplayString	[ebp+20]	; Error message
	call	CrLf
	mov		edx, 0
	mov		eax, 0
	mov		[edi], eax

	mov		ebx, 0
	mov		ecx, 50

	; Same loop as reset_esi. Runs when there is an invalid number
reset_esi_error:
	mov		esi, [ebp+12]
	mov		[esi+ebx], eax		; This element of esi is now zero
	inc		ebx
	loop	reset_esi_error

	pop		ecx					; Restore outer loop counter
	jmp		read_val_loop

read_val_end:
	pop		esi
	pop		edi
	pop		edx
	pop		ecx
	pop		ebx
	pop		eax
	pop		ebp
	ret		24
ReadVal		ENDP
; -----------------------------------------------------------------------------------------------------------------------------------------------

; Sum Process -----------------------------------------------------------------------------------------------------------------------------------
	; Purpose: Sums the 10 numbers stored in int_list.
	; Receives: list_sum @, int_list @
	; Returns: Nothing
	; Preconditions: Parameters must be pushed onto stack in the order stated by Stack Frame State.
	; Registers Changed: eax, ebx, ecx, esi, ebp

sum		PROC
	push	ebp
	mov		ebp, esp
	push	eax
	push	ebx
	push	ecx
	push	edx
	push	esi
	push	edi

	; __________Stack_Frame_State___________
	; old ebp			|	[ebp]			
	; return @			|	[ebp+4]		
	; list_sum @		|	[ebp+8]
	; int_list @ 		|	[ebp+12]
	; ______________________________________
	
; Set up registers
	mov		ecx, 10
	mov		esi, [ebp+12]		; esi contains int_list @
	add		esi, 4				; Start on the second element of int_list, because for some reason the first element is always 0.
	mov		eax, [ebp+8]		; eax contains list_sum @
	mov		ebx, 0
	mov		edi, 2147483647		; The largest valid number (2^31 - 1)

	; Add together the elements of int_list.
	; If an element is negative, subtract it instead
sum_loop:
	mov		edx, 0
	cmp		edi, [esi]
	jg		negate
	add		ebx, [esi]
negate:
	mov		edx, [esi]
	neg		edx
	sub		ebx, edx
	add		esi, 4
	loop	sum_loop

	mov		[eax], ebx

	pop		edi
	pop		esi
	pop		edx
	pop		ecx
	pop		ebx
	pop		eax
	pop		ebp
	ret		8
sum		ENDP

; -----------------------------------------------------------------------------------------------------------------------------------------------

; Average Process -------------------------------------------------------------------------------------------------------------------------------
	; Purpose: Calculates the average of the numbers in int_list.
	; Receives: list_avg @, list_sum
	; Returns: Nothing
	; Preconditions: Parameters must be pushed onto stack in the order stated by Stack Frame State.
	; Registers Changed: eax, ebx, edi, ebp

average		PROC
	push	ebp
	mov		ebp, esp
	push	eax
	push	ebx
	push	edi

	; __________Stack_Frame_State___________
	; old ebp			|	[ebp]			
	; return @			|	[ebp+4]		
	; list_avg @		|	[ebp+8]
	; list_sum			|	[ebp+12]
	; ______________________________________

; Set up registers
	mov		ebx, 10
	mov		eax, [ebp+12]
	mov		edi, [ebp+8]

; Math
	mov		edx, 0
	cdq
	idiv	ebx
	mov		[edi], eax

	pop		edi
	pop		ebx
	pop		eax
	pop		ebp
	ret		8
average		ENDP

; -----------------------------------------------------------------------------------------------------------------------------------------------

; WriteVal Process ------------------------------------------------------------------------------------------------------------------------------
	; Purpose: Converts an integer to a string, then displays a descriptive message and displays that integer as a string.
	; Receives: user_int @
	; Returns: integer, message @
	; Preconditions: Parameters must be pushed onto stack in the order stated by Stack Frame State.
	; Registers Changed: eax, ebx, ecx, edx, edi, ebp

WriteVal	PROC
	push	ebp
	mov		ebp, esp
	push	eax
	push	ebx
	push	ecx
	push	edx
	push	edi
	push	esi

	; __________Stack_Frame_State___________
	; old ebp			|	[ebp]			
	; return @			|	[ebp+4]		
	; user_int @		|	[ebp+8]
	; integer			|	[ebp+12]			; This is a generalized procedure, so integer and message will depend on which call is made.
	; message @ 		|	[ebp+16]
	; ______________________________________

	mov		edi, [ebp+8]		; edi contains user_int @ (a BYTE array of length 50). Used to store the ASCII codes for each digit
	mov		eax, [ebp+12]		; eax contains the value of the integer to be converted to string.
	mov		ebx, 10
	mov		ecx, -1
	mov		esi, 0

	; Here check to see if the number is negative. If so, get its 2's complement and add a minus at the beginning of user_int.
check_sign:
	cmp		eax, esi
	jg		setup_loop
	neg		eax
	push	eax
	mov		eax, 45			; ASCII "-"
	stosb
	pop		eax
	mov		edx, 0
	
setup_loop:
	push	eax					; Save eax for use in length_loop

	; Similar to conversion_loop. The purpose is to iterate through a number of times equal to the number of digits in eax.
	; ecx keeps track of the number of digits minus 1
length_loop:
	mov		edx, 0
	div		ebx
	inc		ecx
	cmp		eax, 0
	jne		length_loop
	pop		eax					; Restore eax to value of integer
	
	add		edi, ecx			; Add to edi the length of the integer minus 1. We will work backward from there to the beginning of edi
	std							; Set direction flag to work backward through edi, since we work backward through eax
	
	; This loop works by dividing the integer in eax by ten on each iteration.
	; This stores the end digit in edx. The digit is moved to eax where 48 is added to it in order to convert to ASCII code.
	; The loop is finished when we run out of numbers (eax = 0).
conversion_loop:
	mov		edx, 0
	div		ebx
	push	eax
	mov		eax, edx
	add		eax, 48
	stosb
	pop		eax
	cmp		eax, 0
	je		display
	jmp		conversion_loop

	; Displays a descriptive message and the string in user_int.
display:
	DisplayString	[ebp+16]
	DisplayString	[ebp+8]

; Prep registers for use in reset_edi loop
	mov		eax, 0
	mov		ebx, 0
	mov		ecx, 50

	; Reset user_int to an array of zeros so that it can be used again for conversion
reset_edi:
	mov		edi, [ebp+8]
	mov		[edi+ebx], eax		; This element of edi is now zero
	inc		ebx
	loop	reset_edi

	pop		esi
	pop		edi
	pop		edx
	pop		ecx
	pop		ebx
	pop		eax
	pop		ebp
	ret		12
WriteVal	ENDP
; -----------------------------------------------------------------------------------------------------------------------------------------------

; Goodbye Process -------------------------------------------------------------------------------------------------------------------------------
	; Purpose: Displays parting message
	; Receives: goodbye_mess @
	; Returns: goodbye_mess
	; Preconditions: Parameters must be pushed onto stack in the order stated by Stack Frame State.
	; Registers Changed: ebp

goodbye		PROC
	push	ebp
	mov		ebp, esp

	; __________Stack_Frame_State___________
	; old ebp			|	[ebp]			
	; return @			|	[ebp+4]		
	; goodbye_mess @	|	[ebp+8]
	; ______________________________________

	DisplayString	[ebp+8]
	call	CrLf

	pop		ebp
	ret		4
goodbye		ENDP
; -----------------------------------------------------------------------------------------------------------------------------------------------

END main
