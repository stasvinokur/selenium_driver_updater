import os
import pytest
import time
from pathlib import Path
import shutil
import zipfile
import tarfile
from selenium_driver_updater.util.extractor import Extractor

base_dir = os.path.dirname(os.path.abspath(__file__))

@pytest.fixture(scope="module")
def setup_paths():
    out_path = os.path.join(base_dir, 'archive')
    zip_archive_path = os.path.join(out_path, 'geckodriver-v0.29.0-win64.zip')
    tar_archive_path = os.path.join(out_path, 'geckodriver-v0.29.1-macos-aarch64.tar.gz')
    tar_xz_archive_path = os.path.join(out_path, 'Opera_78.0.4093.112_Autoupdate_arm64.tar.xz')

    return {
        "out_path": out_path,
        "zip_archive_path": zip_archive_path,
        "tar_archive_path": tar_archive_path,
        "tar_xz_archive_path": tar_xz_archive_path
    }

@pytest.fixture(autouse=True)
def measure_time():
    start_time = time.time()
    yield
    end_time = time.time() - start_time
    print(f"Test duration: {end_time:.3f} seconds")

def test_extract_all_zip_archive_failure(setup_paths):
    with pytest.raises(FileNotFoundError):
        Extractor.extract_all_zip_archive(archive_path="invalid_path.zip", out_path=setup_paths["out_path"])

def test_extract_all_tar_gz_archive_failure(setup_paths):
    with pytest.raises(FileNotFoundError):
        Extractor.extract_all_tar_gz_archive(archive_path="invalid_path.tar.gz", out_path=setup_paths["out_path"])

def test_extract_all_zip_archive_with_specific_name_failure(setup_paths):
    with pytest.raises(FileNotFoundError):
        Extractor.extract_all_zip_archive_with_specific_name(
            archive_path="invalid_path.zip",
            out_path=setup_paths["out_path"],
            delete_archive=False,
            filename='geckodriver.exe',
            filename_replace='geckodriverzip'
        )

def test_extract_all_tar_archive_with_specific_name_failure(setup_paths):
    with pytest.raises(FileNotFoundError):
        Extractor.extract_all_zip_archive_with_specific_name(
            archive_path="invalid_path.tar.gz",
            out_path=setup_paths["out_path"],
            delete_archive=False,
            filename='geckodriver',
            filename_replace='geckodrivertar'
        )

def test_extract_all_tar_xz_archive_failure(setup_paths):
    with pytest.raises(FileNotFoundError):
        Extractor.extract_all_tar_xz_archive(
            archive_path="invalid_path.tar.xz",
            out_path=setup_paths["out_path"]
        )

def test_extract_all_zip_archive(setup_paths):
    Extractor.extract_all_zip_archive(
        archive_path=setup_paths["zip_archive_path"],
        out_path=setup_paths["out_path"],
        delete_archive=False
    )

    geckodriver_path = os.path.join(setup_paths["out_path"], 'geckodriver.exe')
    assert Path(geckodriver_path).exists()
    Path(geckodriver_path).unlink()
    assert not Path(geckodriver_path).exists()

def test_extract_all_tar_gz_archive(setup_paths):
    Extractor.extract_all_tar_gz_archive(
        archive_path=setup_paths["tar_archive_path"],
        out_path=setup_paths["out_path"],
        delete_archive=False
    )

    geckodriver_path = os.path.join(setup_paths["out_path"], 'geckodriver')
    assert Path(geckodriver_path).exists()
    Path(geckodriver_path).unlink()
    assert not Path(geckodriver_path).exists()

def test_extract_all_zip_archive_with_specific_name(setup_paths):
    # Проверка содержимого архива перед извлечением
    with zipfile.ZipFile(setup_paths["zip_archive_path"], 'r') as zip_ref:
        print("Contents of the zip archive:", zip_ref.namelist())

    Extractor.extract_all_zip_archive_with_specific_name(
        archive_path=setup_paths["zip_archive_path"],
        out_path=setup_paths["out_path"],
        delete_archive=False,
        filename='geckodriver.exe',
        filename_replace='geckodriverzip'
    )
    
    geckodriver_path = os.path.join(setup_paths["out_path"], 'geckodriverzip')
    print(f"Checking existence of {geckodriver_path}")
    assert Path(geckodriver_path).exists(), f"Expected file not found: {geckodriver_path}"
    Path(geckodriver_path).unlink()
    assert not Path(geckodriver_path).exists()

def test_extract_all_tar_archive_with_specific_name(setup_paths):
    # Проверка содержимого архива перед извлечением
    with tarfile.open(setup_paths["tar_archive_path"], 'r') as tar_ref:
        print("Contents of the tar archive:", tar_ref.getnames())

    Extractor.extract_all_zip_archive_with_specific_name(
        archive_path=setup_paths["tar_archive_path"],
        out_path=setup_paths["out_path"],
        delete_archive=False,
        filename='geckodriver',
        filename_replace='geckodrivertar'
    )
    
    geckodriver_path = os.path.join(setup_paths["out_path"], 'geckodrivertar')
    print(f"Checking existence of {geckodriver_path}")
    assert Path(geckodriver_path).exists(), f"Expected file not found: {geckodriver_path}"
    Path(geckodriver_path).unlink()
    assert not Path(geckodriver_path).exists()

def test_extract_all_tar_xz_archive(setup_paths):
    Extractor.extract_all_tar_xz_archive(
        archive_path=setup_paths["tar_xz_archive_path"],
        out_path=setup_paths["out_path"],
        delete_archive=False
    )

    opera_path = os.path.join(setup_paths["out_path"], 'Opera.app')
    assert Path(opera_path).exists()
    shutil.rmtree(opera_path)
    assert not Path(opera_path).exists()