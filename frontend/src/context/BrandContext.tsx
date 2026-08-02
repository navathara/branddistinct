import { createContext, useContext, useState } from "react";
import type { ReactNode } from "react";

type BrandContextType = {
    brand: any;
    setBrand: (brand: any) => void;
    clearBrand: () => void;
};

const BrandContext = createContext<BrandContextType | null>(null);

export function BrandProvider({
    children,
}: {
    children: ReactNode;
}) {
    const [brand, setBrand] = useState<any>(null);

    function clearBrand() {
        setBrand(null);
    }

    return (
        <BrandContext.Provider
            value={{
                brand,
                setBrand,
                clearBrand,
            }}
        >
            {children}
        </BrandContext.Provider>
    );
}

export function useBrand() {
    const context = useContext(BrandContext);

    if (!context) {
        throw new Error("useBrand must be used inside BrandProvider");
    }

    return context;
}