import SignIn from '@/components/SignIn'
import useAuth from '@/utils/hooks/useAuth'
import Board from "@/components/Board";
import {useEffect, useState} from "react";

export default function Home() {
    const [authenticated, setIsAuth] = useState(false)

    useEffect(() => {
        const {authenticated: auth} = useAuth()
        setIsAuth(auth)
    })
    return <>{authenticated ? <Board/> : <SignIn/>}</>
}
