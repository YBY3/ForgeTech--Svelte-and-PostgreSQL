export const load = async ({ locals }) => {
    if (locals.user) {
        return { user: locals.user };
    }
    else {
        return { user: null };
    }
};