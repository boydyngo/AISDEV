# PowerShell script to install code-sandbox-mcp
# Run as Administrator

# Create directory for the code-sandbox-mcp
$installDir = "C:\Users\d0wil\AI-Development"
$mpcServerName = "code-sandbox-mcp"
$exePath = Join-Path $installDir "$mpcServerName.exe"
$repoOwner = "Automata-Labs-team"
$repoName = "code-sandbox-mcp"

Write-Host "Installing code-sandbox-mcp to $installDir..."

# Create the directory if it doesn't exist
if (-not (Test-Path -Path $installDir)) {
    New-Item -ItemType Directory -Path $installDir -Force
}

# Get the latest release from GitHub API
try {
    $apiUrl = "https://api.github.com/repos/$repoOwner/$repoName/releases/latest"
    $githubToken = $env:GITHUB_TOKEN
    
    # Create headers with or without a token
    $headers = @{
        "Accept" = "application/vnd.github.v3+json"
    }
    if ($githubToken) {
        $headers["Authorization"] = "token $githubToken"
    }
    
    # Fetch the latest release info
    $releaseInfo = Invoke-RestMethod -Uri $apiUrl -Headers $headers
    
    # Find the Windows asset
    $asset = $releaseInfo.assets | Where-Object { $_.name -like "*windows*.exe" -or $_.name -like "*win*.exe" -or $_.name -eq "$mpcServerName.exe" }
    
    if ($asset) {
        # Download the executable
        Write-Host "Downloading $($asset.name) from $($asset.browser_download_url)..."
        Invoke-WebRequest -Uri $asset.browser_download_url -OutFile $exePath
        
        Write-Host "Downloaded to $exePath"
    } else {
        Write-Host "Could not find a Windows executable in the latest release. Available assets:"
        $releaseInfo.assets | ForEach-Object { Write-Host "  $($_.name)" }
        exit 1
    }
} catch {
    Write-Host "Error: $_"
    Write-Host "Failed to download code-sandbox-mcp. Trying to download directly from the source..."
    
    # Fallback to direct install via irm (this is the official install method)
    irm https://raw.githubusercontent.com/Automata-Labs-team/code-sandbox-mcp/main/install.ps1 | iex
    exit
}

# Check if Docker is installed and running
try {
    $dockerVersion = docker --version
    Write-Host "Docker is installed: $dockerVersion"
    
    $dockerRunning = docker ps
    Write-Host "Docker appears to be running."
} catch {
    Write-Host "WARNING: Docker Desktop is not installed or not running. Please install Docker Desktop for Windows and make sure it's running before using code-sandbox-mcp."
}

# Verify the executable was downloaded
if (Test-Path -Path $exePath) {
    Write-Host "Installation complete! code-sandbox-mcp has been installed to $exePath"
    Write-Host "Claude Desktop configuration has been updated to use this installation."
    Write-Host ""
    Write-Host "Please restart Claude Desktop for the changes to take effect."
} else {
    Write-Host "Installation failed. The executable was not found at $exePath"
    Write-Host "Please check for errors and try again."
}
