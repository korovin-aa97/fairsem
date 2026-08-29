class Fairsem < Formula
  include Language::Python::Shebang

  desc "Fair, observable semaphore for local Linux commands"
  homepage "https://github.com/korovin-aa97/fairsem"
  url "https://github.com/korovin-aa97/fairsem/releases/download/v0.1.0/fairsem-v0.1.0.tar.gz"
  sha256 "3e2562d992eb003f29c9c39d43f4c3ec708eed6f24eebf3aa1aee262b98c9672"
  license "MIT"

  depends_on :linux
  depends_on "python@3.13"

  def install
    rewrite_shebang detected_python_shebang, "bin/fairsem"
    bin.install "bin/fairsem"
    man1.install "man/fairsem.1"
  end

  test do
    assert_match "fairsem 0.1.0", shell_output("#{bin}/fairsem --version")
    ENV["FAIRSEM_STATE_DIR"] = testpath/"state"
    system bin/"fairsem", "run", "--name", "homebrew", "--", "true"
  end
end
