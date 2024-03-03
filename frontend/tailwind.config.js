module.exports = {
    dark: false,
    theme: {
        extend: {
            colors: {
                primary: '#092E43',
                secondary: '#DA8252',
                white: '#FFF',
            }
        }
    },
    plugins: [
        require('@tailwindcss/forms')
    ]
}