"use client";


import {
    useEffect,
    useState,
} from "react";


import {
    getThreats,
} from "@/services/threatService";


import {
    Threat,
} from "@/types/threat";


export function useThreats() {

    const [
        threats,
        setThreats,
    ] = useState<Threat[]>([]);


    const [
        loading,
        setLoading,
    ] = useState(true);


    const [
        error,
        setError,
    ] = useState<string | null>(null);


    useEffect(() => {

        async function loadThreats() {

            try {

                setLoading(true);


                const data =
                    await getThreats();


                setThreats(data);


            } catch (err) {

                setError(
                    err instanceof Error
                        ? err.message
                        : "Failed to load threats"
                );


            } finally {

                setLoading(false);

            }

        }


        loadThreats();

    }, []);


    return {

        threats,

        loading,

        error,

    };

}