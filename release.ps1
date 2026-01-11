param(
    [Parameter(Mandatory=$true, HelpMessage="Version to release (e.g. 1.0.0)")]
    [string]$Version
)

# Проверка формата версии (X.Y.Z)
if ($Version -notmatch '^\d+\.\d+\.\d+$') {
    Write-Error "Ошибка: Версия должна быть в формате X.Y.Z (например, 1.0.0)"
    exit 1
}

$Tag = "v$Version"

# Проверка, существует ли тег локально
if (git tag -l $Tag) {
    Write-Error "Ошибка: Тег $Tag уже существует локально."
    exit 1
}

# Подтверждение
$Confirmation = Read-Host "Вы собираетесь создать тег $Tag и отправить его в origin. Продолжить? (y/n)"
if ($Confirmation -ne 'y') {
    Write-Host "Отмена."
    exit 0
}

# Создание тега
Write-Host "Создание тега $Tag..."
git tag $Tag

if ($LASTEXITCODE -eq 0) {
    # Отправка тега
    Write-Host "Отправка тега $Tag в репозиторий..."
    git push origin $Tag
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Успешно! GitHub Actions должен скоро начать сборку для $Tag."
        Write-Host "Проверить статус: https://github.com/<ваш_пользователь>/sims_mods_holder/actions"
    } else {
        Write-Error "Ошибка при отправке тега."
    }
} else {
    Write-Error "Ошибка при создании тега."
}
