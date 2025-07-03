import React from "react";

interface CountryPageProps {
    countryCode: string;
}

const CountryPage: React.FC<CountryPageProps> = (props: CountryPageProps) => {
    const { countryCode } = props;

    return (
        <div>CountryPage</div>
    )
}

export default CountryPage;