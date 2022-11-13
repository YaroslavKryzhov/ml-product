import {
  AppBar,
  Checkbox,
  Chip,
  FormControlLabel,
  Paper,
  Stack,
  TextField,
  Toolbar,
} from "@mui/material";
import LoadingButton from "@mui/lab/LoadingButton";
import React, { useEffect, useLayoutEffect, useState } from "react";
import { CenteredContainer, helperTextProps } from "components/muiOverride";
import { pathify, useAppDispatch, useSESelector } from "ducks/hooks";
import {
  authReset,
  changeEmail,
  changePasswordInput,
  changeSecondPasswordInput,
} from "ducks/reducers/auth";
import {
  AppPage,
  AuthPage,
  DocumentPage,
  WorkPage,
} from "ducks/reducers/types";
import EmailValidator from "email-validator";
import {
  useAuthMutation,
  useRegisterMutation,
} from "ducks/reducers/api/auth.api";
import { theme } from "globalStyle/theme";
import { PASSWORD_ERROR, ALREADY_EXIST, BAD_LOGIN } from "./const";
import { passwordValidate } from "./helpers";
import { useNavigate, useLocation } from "react-router-dom";
import { addNotice, SnackBarType } from "ducks/reducers/notices";

export const Authentication: React.FC = () => {
  const { passwordInput, emailInput, secondPasswordInput } = useSESelector(
    (state) => state.auth
  );
  const dispatch = useAppDispatch();
  const [isFirstTry, setIsFirstTry] = useState(true);
  const { pathname } = useLocation();
  const navigate = useNavigate();
  const [register, { isLoading: isRegLoading, isSuccess: isRegSuccess }] =
    useRegisterMutation();
  const [
    auth,
    { isLoading: isAuthLoading, isSuccess: isAuthSuccess, data: authResponse },
  ] = useAuthMutation();
  const isLoading = isRegLoading || isAuthLoading;

  const isEmailError = !EmailValidator.validate(emailInput);
  const isReg = !!pathname.match(
    pathify([AppPage.Authentication, AuthPage.register])
  );
  const isPasswordError =
    (isReg && !passwordInput) || !passwordValidate(passwordInput);
  const isSecondPasswordError =
    isReg &&
    (!secondPasswordInput ||
      !passwordValidate(secondPasswordInput) ||
      secondPasswordInput !== passwordInput);

  const authCallback = () => {
    setIsFirstTry(false);
    if (isEmailError || isPasswordError || isSecondPasswordError) return;

    if (!isReg)
      auth({ username: emailInput, password: passwordInput }).then(
        (res: any) => {
          (res as any).error?.data?.detail === BAD_LOGIN &&
            dispatch(
              addNotice({
                label: "Ошибка. Попробуйте еще раз.",
                type: SnackBarType.error,
                id: Date.now(),
              })
            );

          dispatch(authReset());
        }
      );
    else
      register({ email: emailInput, password: passwordInput }).then(
        (res) =>
          (res as any).error.data.detail === ALREADY_EXIST &&
          dispatch(
            addNotice({
              label: "Такой пользователь уже существует",
              type: SnackBarType.error,
              id: Date.now(),
            })
          )
      );
  };

  useEffect(() => setIsFirstTry(true), [isReg]);

  useLayoutEffect(() => {
    if (isAuthSuccess) {
      localStorage.authToken = authResponse?.access_token;

      navigate(
        pathify([AppPage.Workplace, WorkPage.Documents, DocumentPage.List])
      );
    }
  }, [isAuthSuccess, authResponse, navigate]);

  useLayoutEffect(() => {
    if (isRegSuccess) {
      auth({ username: emailInput, password: passwordInput });
    }
  }, [auth, emailInput, isRegSuccess, passwordInput]);

  return (
    <Stack direction="column" sx={{ height: "100vh" }}>
      <AppBar position="static">
        <Toolbar sx={{ justifyContent: "space-between" }}>
          <Chip
            sx={{
              backgroundColor: "primary.light",
              color: "primary.contrastText",
              "&:hover": {
                backgroundColor: "secondary.dark",
              },
            }}
            clickable
            onClick={() => {
              isReg ? navigate(AuthPage.auth) : navigate(AuthPage.register);

              setIsFirstTry(true);
            }}
            label={isReg ? "Авторизация" : "Регистрация"}
          />
        </Toolbar>
      </AppBar>
      <CenteredContainer sx={{ flexGrow: 1 }}>
        <Paper
          sx={{ maxWidth: 657, width: "100%", p: theme.spacing(4) }}
          elevation={3}
        >
          <Stack direction="column">
            <TextField
              size="small"
              type="email"
              label="Почта"
              value={emailInput}
              error={!isFirstTry && isEmailError}
              helperText={!isFirstTry && isEmailError ? "Неверная почта" : " "}
              onChange={(e) => dispatch(changeEmail(e.target.value))}
              FormHelperTextProps={helperTextProps}
              sx={{ mb: theme.spacing(4) }}
            />
            <TextField
              size="small"
              type="password"
              label="Пароль"
              value={passwordInput}
              onChange={(e) => dispatch(changePasswordInput(e.target.value))}
              helperText={!isFirstTry && isPasswordError ? PASSWORD_ERROR : " "}
              error={!isFirstTry && isPasswordError}
              FormHelperTextProps={helperTextProps}
              sx={{ mb: theme.spacing(4) }}
            />
            {isReg && (
              <TextField
                size="small"
                type="password"
                label="Повторите пароль"
                value={secondPasswordInput}
                FormHelperTextProps={helperTextProps}
                onChange={(e) =>
                  dispatch(changeSecondPasswordInput(e.target.value))
                }
                sx={{ mb: theme.spacing(4) }}
                error={!isFirstTry && isSecondPasswordError}
                helperText={
                  !isFirstTry && isSecondPasswordError
                    ? secondPasswordInput !== passwordInput
                      ? "Пароли не совпадают"
                      : PASSWORD_ERROR
                    : " "
                }
              />
            )}
            {!isReg && (
              <FormControlLabel
                control={<Checkbox size="small" />}
                label="Запомнить меня"
                sx={{ mt: theme.spacing(4) }}
              />
            )}
            <LoadingButton
              loading={isLoading}
              size="small"
              variant="contained"
              onClick={authCallback}
              sx={{
                mt: theme.spacing(2),
              }}
            >
              {isReg ? "Зарегистрироваться" : "Войти"}
            </LoadingButton>
          </Stack>
        </Paper>
      </CenteredContainer>
    </Stack>
  );
};
