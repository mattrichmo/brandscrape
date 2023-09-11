const shape = {
    "brandName": "", // name of the brand
    "brandWebsite": "", // website of the brand
    "brandPresence": [ // array of social media presence
        {
            "platform": "", // social media platform
            "url": "", // URL of the brand's profile on the platform
            "username": "" // username of the brand on the platform
        }
    ],
    "brandLogo": [ // array of logos for the brand
        {
            "fileName": "", // name of the logo file
            "svgPath": "", // path to the SVG file for the logo
            "svgData": { // object containing metadata and raw SVG data for the logo
                "meta": {
                    "width": "", // width of the logo
                    "height": "", // height of the logo
                    "viewbox": "", // viewBox attribute of the SVG element
                    "fill": "" // fill attribute of the SVG element
                },
                "svgRaw": "" // raw SVG data for the logo
            }
        }
    ],
    "brandColors": [ // array of brand colors
        {
            "meta": { // object containing metadata for the color
                "primary": false, // whether the color is a primary brand color
                "secondary": true, // whether the color is a secondary brand color
                "tertiary": false, // whether the color is a tertiary brand color
                "quaternary": false, // whether the color is a quaternary brand color
                "priority": 0 // priority of the color, with 0 being the highest
            },
            "colorName": "", // name of the color
            "colorHex": "", // hexadecimal value of the color
            "colorRGB": "", // RGB value of the color
            "colorCMYK": "", // CMYK value of the color
            "colorPantone": "" // Pantone value of the color
        }
    ]
};