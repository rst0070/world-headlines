function googleTranslateElementInit() {
    new google.translate.TranslateElement(
        {
            autoDisplay: true,
            layout: google.translate.TranslateElement.InlineLayout.HORIZONTAL
                    
        }, 
        'google_translate_element'
    );
}