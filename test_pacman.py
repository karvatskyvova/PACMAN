import pytest
import json
from PacmanMenu import Increase, Decrease, SaveData, ReadData


@pytest.mark.parametrize("value, valueRange, expected", [(3, (1, 4), 4), (4, (1, 4), 1)])
def test_Increase(value, valueRange, expected):
    assert Increase(value, valueRange) == expected


@pytest.mark.parametrize("value, valueRange, expected", [(3, (1, 4), 2), (1, (1, 4), 4)])
def test_Decrease(value, valueRange, expected):
    assert Decrease(value, valueRange) == expected


def test_SaveData(tmp_path):
    saveFile = tmp_path / "test_save.json"  # Створюємо тимчасовий файл для зберігання даних
    SaveData(saveFile, 1, 5, 10)  # Викликаємо функцію SaveData для збереження даних

    # Перевіряємо, чи файли існують і чи містять вони очікувані дані
    assert saveFile.exists()
    with open(saveFile, 'r') as f:
        data = json.load(f)
        assert data["Level"] == 1
        assert data["Number of Enemies"] == 5
        assert data["Enemies Speed"] == 10


def test_ReadData(tmp_path):
    # Створюємо тимчасовий файл та записуємо в нього дані
    saveFile = tmp_path / "test_read.json"
    data = {"Level": 1, "Number of Enemies": 2, "Enemies Speed": 3}
    with open(saveFile, 'w') as f:
        json.dump(data, f)

    # Викликаємо функцію ReadData та перевіряємо, чи повертаються очікувані дані
    result = ReadData(saveFile, 2, (1, 4), (1, 4))
    assert result == (1, 2, 3)

    # Перевірка на випадок, коли дані у файлі некоректні
    invalidDataFile = tmp_path / "invalid_data.json"
    invalid_data = {"Level": 3, "Number of Enemies": 5, "Enemies Speed": 5}
    with open(invalidDataFile, 'w') as f:
        json.dump(invalid_data, f)
    result = ReadData(invalidDataFile, 2, (1, 4), (1, 4))
    assert result is None

    # Перевірка на випадок, коли файлу не існує
    nonExistingFile = tmp_path / "non_existing.json"
    result = ReadData(nonExistingFile, 2, (1, 4), (1, 4))
    assert result is None
