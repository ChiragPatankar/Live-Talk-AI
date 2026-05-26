# Create checkpoints directory if it doesn't exist
New-Item -ItemType Directory -Force -Path "./checkpoints" | Out-Null
New-Item -ItemType Directory -Force -Path "./gfpgan/weights" | Out-Null

# Download model files
$files = @(
    @{
        url = "https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2-rc/mapping_00109-model.pth.tar"
        output = "./checkpoints/mapping_00109-model.pth.tar"
    },
    @{
        url = "https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2-rc/mapping_00229-model.pth.tar"
        output = "./checkpoints/mapping_00229-model.pth.tar"
    },
    @{
        url = "https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2-rc/SadTalker_V0.0.2_256.safetensors"
        output = "./checkpoints/SadTalker_V0.0.2_256.safetensors"
    },
    @{
        url = "https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2-rc/SadTalker_V0.0.2_512.safetensors"
        output = "./checkpoints/SadTalker_V0.0.2_512.safetensors"
    },
    @{
        url = "https://github.com/xinntao/facexlib/releases/download/v0.1.0/alignment_WFLW_4HG.pth"
        output = "./gfpgan/weights/alignment_WFLW_4HG.pth"
    },
    @{
        url = "https://github.com/xinntao/facexlib/releases/download/v0.1.0/detection_Resnet50_Final.pth"
        output = "./gfpgan/weights/detection_Resnet50_Final.pth"
    },
    @{
        url = "https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.4.pth"
        output = "./gfpgan/weights/GFPGANv1.4.pth"
    },
    @{
        url = "https://github.com/xinntao/facexlib/releases/download/v0.2.2/parsing_parsenet.pth"
        output = "./gfpgan/weights/parsing_parsenet.pth"
    }
)

foreach ($file in $files) {
    if (-not (Test-Path $file.output)) {
        Write-Host "Downloading $($file.url) to $($file.output)..."
        Invoke-WebRequest -Uri $file.url -OutFile $file.output
    } else {
        Write-Host "File $($file.output) already exists, skipping..."
    }
}

Write-Host "Download complete!" 