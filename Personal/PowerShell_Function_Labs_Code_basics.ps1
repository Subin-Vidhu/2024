Write-Host "hey subin"

function Say-Hello {
    Write-Host "Hello, World!"
}

# Call the function
Say-Hello

function Greet-User {
    param (
        [string]$Name
    )
    Write-Host "Hello, $Name!"
}

# Call the function with a parameter
Greet-User -Name "Alice"

function Add-Numbers {
    param (
        [int]$a,
        [int]$b
    )
    return $a + $b
}

# Call the function
$result = Add-Numbers -a 5 -b 10
Write-Host "The sum is: $result"


function Display-Info {
    param (
        [string]$Name = "User",
        [int]$Age = 30
    )
    Write-Host "Name: $Name, Age: $Age"
}

# Call the function without parameters
Display-Info

# Call the function with parameters
Display-Info -Name "John" -Age 25


function Get-FileList {
    param (
        [string]$Directory = "."
    )
    Get-ChildItem -Path $Directory
}

# Call the function
Get-FileList -Directory "."

function Test-FileExists {
    param (
        [string]$FilePath
    )
    if (Test-Path $FilePath) {
        Write-Host "File exists."
    } else {
        Write-Host "File does not exist."
    }
}

# Call the function
Test-FileExists -FilePath "C:\Temp\myfile.txt"

function Get-Factorial {
    param (
        [int]$Number
    )
    if ($Number -eq 0) {
        return 1
    } else {
        return $Number * (Get-Factorial ($Number - 1))
    }
}

# Call the function
$factorial = Get-Factorial -Number 5
Write-Host "Factorial of 5 is: $factorial"

function Write-Log {
    param (
        [string]$LogMessage,
        [string]$LogFile = "C:\Users\ASUS\AppData\Local\Temp\logfile.txt"
    )
    Add-Content -Path $LogFile -Value $LogMessage
}

# Call the function
Write-Log -LogMessage "This is a log message using powershell." -LogFile "C:\Users\ASUS\AppData\Local\Temp\mylog.txt"


function Get-DateTime {
    return Get-Date
}

# Call the function
$currentDateTime = Get-DateTime
Write-Host "Current date and time: $currentDateTime"


function Get-Square {
    param (
        [Parameter(ValueFromPipeline=$true)]
        [int]$Number
    )
    process {
        $Number * $Number
    }
}

# Call the function with pipeline
1..5 | Get-Square
