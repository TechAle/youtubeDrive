from seleniumbase import SB

with SB(uc=True, headed=True) as driver:
    driver.get("https://accounts.google.com/o/oauth2/v2/auth/oauthchooseaccount?redirect_uri=https%3A%2F%2Fdevelopers.google.com%2Foauthplayground&prompt=consent&response_type=code&client_id=407408718192.apps.googleusercontent.com&scope=email&access_type=offline&flowName=GeneralOAuthFlow")
    driver.type("#identifierId", "alessandro.condello.email@gmail.com")
    driver.click("#identifierNext > div > button")

    driver.type("#password > div.aCsJod.oJeWuf > div > div.Xb9hP > input", "Alex90990?Gmail")
    driver.click("#passwordNext > div > button")

    driver.save_screenshot("test.png")