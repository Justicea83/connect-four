import ApiService from "@/services/ApiService";

export default function useAuth() {
    const token = typeof window !== "undefined" ? window.localStorage.getItem('token') : false
    const signIn = async (payload) => {
        try {
            const resp = await ApiService.fetchData({
                url: '/api/user/token/',
                method: 'POST',
                data: payload
            })
            if (resp.data.token) {
                const {token, user_id, name} = resp.data
                window.localStorage.setItem('token', token)
                window.localStorage.setItem('userId', user_id)
                window.localStorage.setItem('name', name)

                return {
                    status: 'success',
                    message: '',
                }
            }
        } catch (e) {
            const errors = e.response.data
            const firstError = errors[Object.keys(errors)[0]][0]
            console.log(firstError)
            return {
                status: 'failed',
                message: firstError || errors.toString(),
            }
        }
    }

    return {
        authenticated: token !== null,
        signIn,
    }
}