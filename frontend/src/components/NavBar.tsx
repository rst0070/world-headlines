import React from "react";

interface NavBarProps {
    countryCodes: string[];
}

const NavBar: React.FC<NavBarProps> = (props: NavBarProps) => {
    const { countryCodes } = props;

    return (
        <ul>
            {countryCodes.map((countryCode) => (
                <li key={countryCode}>
                    <a href={`/country/${countryCode}`}>
                        {countryCode}
                    </a>
                </li>
            ))}
        </ul>
    )
}

export default NavBar;