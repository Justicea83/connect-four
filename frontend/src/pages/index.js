import SignIn from '@/components/SignIn'
import useAuth from "@/utils/hooks/useAuth";
import Game from "@/components/Game";
//import styles from '@/styles/Home.module.css'

export default function Home() {
    const {authenticated} = useAuth()
    return (
        <>
            {authenticated ? <Game/> : <SignIn/>}
        </>
    )
}
