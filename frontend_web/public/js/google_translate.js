function googleTranslateElementInit() {
    const userLang = navigator.language || navigator.userLanguage; 

    console.log("user language is "+userLang)
    setCookie('googtrans', `/auto/${userLang}`,1)
    
    new google.translate.TranslateElement(
        {
            autoDisplay: true,
            layout: google.translate.TranslateElement.InlineLayout.HORIZONTAL
        }, 
        'google_translate_element'
    );
}