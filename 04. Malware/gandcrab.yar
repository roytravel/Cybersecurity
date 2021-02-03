rule Gandcrab
{
    meta:
        Author      = "roytravel"
        Maltype     = "Ransomware"
        Malname     = "Gandcrab"
        Filetype    = "exe"
        Description = "How to Detect Gandcrab Effectively"

    strings:
        $API1  = "DecodePointer" //266
        $API2  = "DeleteCriticalSection" //266
        $API3  = "FreeEnvironmentStringsW" //266
        $API4  = "GetCurrentProcess" //266
        $API5  = "GetCurrentProcessId" //266
        $API6  = "GetCPInfo" //266
        $API7  = "GetLastError" //266
        $API8  = "HeapAlloc" //266
        $API9  = "InitializeCriticalSectionAndSpinCount" //266
        $API10 = "LeaveCriticalSection" //266
        $API11 = "LoadLibrary" //266
        $API12 = "MultiByteToWideChar" //266
        $API13 = "TerminateProcess" //266
        $API14 = "TlsGetValue" //266
        $API15 = "TlsSetValue" //266
        $API16 = "VirtualProtect" //266
        $API17 = "WriteFile" //266
        $API18 = "GetModuleHandle" //267

        $decodeRoutine = { 50 ( 5? | 6A 00 ) 68 00 00 ( 40 00 | 00 60 | 00 03 ) E8 ?? ?? ( FF FF | 00 00 ) }
        $String1 = "QEBHOVQ" wide ascii
        $String2 = "TOKAWUDEJEBA" wide ascii

        $icon1 = { F7 F0 00 00 09 25 DC FD FF EA 00 00 0B C7 DC FD FF CC 64 
        C8 70 4F DC FD FF F5 4F 81 E1 E7 DC FD FB FF D5 40 93 47 DC FD }
        $icon2 = { F3 18 00 00 10 8F DC FD DF FF 80 00 0C 5F DC FD 56 FD DA
        FB 9F 30 DC FD DD F6 FD 1A B6 F7 DC FD EF EB FF E1 C4 C7 DC FD }

    condition:
        ((uint16(0)==0x5A4D and all of ($API*)) or (uint32(0x3c)==0x00000040 and any of ($String*))) 
        and 
        (($decodeRoutine or any of ($String*)) and (any of ($icon*)))
}
